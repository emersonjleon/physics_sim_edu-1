import numpy as np
from .rgb_camera import MujocoRgbCamera
from physics_simulator.simulator import MujocoSimulator as PhysicsSimulator
from synthnova_config import DepthCameraConfig

class MujocoDepthCamera(MujocoRgbCamera):
    """Depth camera sensor for MuJoCo simulation.
    
    This class extends the RGB camera to provide depth sensing capabilities.
    It inherits all functionality from MujocoRgbCamera and adds depth-specific
    features such as depth map retrieval and point cloud generation.
    """
    
    def __init__(self, simulator: PhysicsSimulator, camera_config: DepthCameraConfig):
        """Initialize a depth camera in the MuJoCo simulation.
        
        Args:
            simulator: The physics simulator instance
            camera_config: Configuration object for the depth camera
        """
        super().__init__(simulator, camera_config)

    def get_data(self) -> np.ndarray:
        """Get the latest rendered depth data.
        
        Returns:
            np.ndarray: Depth image as a numpy array with shape (height, width, 1)
                        where each value represents the distance from the camera
        """
        return self.get_depth()

    def get_depth(self):
        """Get the depth map from the current camera view.
        
        Returns:
            np.ndarray: Depth map as a numpy array, with values representing
                       distance from the camera in meters
        """
        _, depth = self.render(depth=True, segmentation=False)
        from physics_simulator.utils.camera_utils import get_real_depth_map

        depth = get_real_depth_map(self.simulator, depth)
        return depth
    
    def get_point_cloud(self) -> np.ndarray:
        """Generate a 3D point cloud from the depth data in world coordinates.
        
        Converts the depth map to a set of 3D points in the world coordinate frame.
        
        Returns:
            np.ndarray: Point cloud as an Nx3 array of (X, Y, Z) points in world frame
        """
        from physics_simulator.utils.camera_utils import (
            get_point_cloud_from_depth, 
            filter_point_cloud,
            get_camera_extrinsic_matrix
        )
        
        # Get depth map
        depth_map = self.get_depth()
        
        # Generate point cloud in camera frame using intrinsic parameters
        point_cloud_camera = get_point_cloud_from_depth(
            depth_image=depth_map,
            fx=self.fx,
            fy=self.fy,
            cx=self.cx,
            cy=self.cy
        )
        
        # Filter the point cloud to remove invalid points
        point_cloud_camera = filter_point_cloud(
            point_cloud_camera,
            min_distance=0.01,
            max_distance=10.0,
            remove_outliers=True,
            outlier_std_factor=2.0
        )
        
        if len(point_cloud_camera) == 0:
            return np.array([]).reshape(0, 3)
        
        # Transform from camera frame to world frame
        with self.simulator.lock:
            # Get camera extrinsic matrix (camera to world transform)
            camera_extrinsic = get_camera_extrinsic_matrix(
                sim=self.simulator,
                camera_name=self.name
            )
        
        # Convert points to homogeneous coordinates
        ones = np.ones((point_cloud_camera.shape[0], 1))
        point_cloud_homogeneous = np.hstack([point_cloud_camera, ones])
        
        # Transform to world coordinates
        point_cloud_world = (camera_extrinsic @ point_cloud_homogeneous.T).T
        
        return point_cloud_world[:, :3]

    def get_point_cloud_wrt_robot(self, robot, downsample_factor=2, max_distance=2.0, 
                                  skip_outlier_removal=True):
        """Transform the depth point cloud to the robot's coordinate frame.
        
        Converts the depth data to a 3D point cloud and transforms it directly from
        camera coordinates to the robot's local coordinate frame (optimized version).
        
        Args:
            robot: The robot object to transform the point cloud relative to
            downsample_factor (int): Factor to downsample the depth image for performance 
                                   (2 = half resolution, 4x speed improvement)
            max_distance (float): Maximum distance to keep points in meters (default: 2.0m)
            skip_outlier_removal (bool): Skip expensive statistical outlier removal for speed
            
        Returns:
            np.ndarray: Point cloud as an Nx3 array of (X, Y, Z) points in robot frame
        """
        from physics_simulator.utils.camera_utils import get_camera_extrinsic_matrix
        from scipy.spatial.transform import Rotation as R
        
        # Get depth map once
        _, depth_map = self.render(depth=True, segmentation=False)
        from physics_simulator.utils.camera_utils import get_real_depth_map
        depth_map = get_real_depth_map(self.simulator, depth_map)
        
        # Downsample for performance if requested
        if downsample_factor > 1:
            depth_map = depth_map[::downsample_factor, ::downsample_factor]
            fx_scaled = self.fx / downsample_factor
            fy_scaled = self.fy / downsample_factor
            cx_scaled = self.cx / downsample_factor
            cy_scaled = self.cy / downsample_factor
        else:
            fx_scaled, fy_scaled, cx_scaled, cy_scaled = self.fx, self.fy, self.cx, self.cy
        
        # Generate point cloud in camera frame (optimized)
        height, width = depth_map.shape
        u, v = np.meshgrid(np.arange(width), np.arange(height))
        
        # Simple distance filtering instead of complex outlier removal for speed
        valid_mask = (depth_map > 0.01) & (depth_map < max_distance) & np.isfinite(depth_map)
        
        if not np.any(valid_mask):
            return np.array([]).reshape(0, 3)
        
        u_valid = u[valid_mask]
        v_valid = v[valid_mask]
        z_valid = depth_map[valid_mask]
        
        # Convert to camera coordinates using pinhole camera model
        x_camera = (u_valid - cx_scaled) * z_valid / fx_scaled
        y_camera = (v_valid - cy_scaled) * z_valid / fy_scaled
        z_camera = z_valid
        
        point_cloud_camera = np.stack([x_camera, y_camera, z_camera], axis=1)
        
        # Apply statistical outlier removal if not skipped (slower but better quality)
        if not skip_outlier_removal:
            from physics_simulator.utils.camera_utils import filter_point_cloud
            point_cloud_camera = filter_point_cloud(
                point_cloud_camera,
                min_distance=0.01,
                max_distance=max_distance,
                remove_outliers=True,
                outlier_std_factor=2.0
            )
            
            if len(point_cloud_camera) == 0:
                return np.array([]).reshape(0, 3)
        
        # Get transformation matrices in one lock for efficiency
        with self.simulator.lock:
            # Get camera extrinsic matrix (camera to world transform)
            camera_extrinsic = get_camera_extrinsic_matrix(
                sim=self.simulator,
                camera_name=self.name
            )
            
            # Get robot pose in world frame
            robot_position, robot_orientation = robot.get_world_pose()
        
        # Compute direct camera-to-robot transformation (skip intermediate world transform)
        robot_rotation_matrix = R.from_quat(robot_orientation).as_matrix()
        world_to_robot = np.eye(4)
        world_to_robot[:3, :3] = robot_rotation_matrix.T
        world_to_robot[:3, 3] = -robot_rotation_matrix.T @ robot_position
        
        # Direct camera-to-robot transformation matrix
        camera_to_robot = world_to_robot @ camera_extrinsic
        
        # Transform points directly from camera to robot frame
        ones = np.ones((len(point_cloud_camera), 1))
        point_cloud_homogeneous = np.hstack([point_cloud_camera, ones])
        point_cloud_robot = (camera_to_robot @ point_cloud_homogeneous.T).T
        
        return point_cloud_robot[:, :3]