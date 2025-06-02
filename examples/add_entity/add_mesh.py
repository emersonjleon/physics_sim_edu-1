#####################################################################################
# Copyright (c) 2023-2025 Galbot. All Rights Reserved.
#
# This software contains confidential and proprietary information of Galbot, Inc.
# ("Confidential Information"). You shall not disclose such Confidential Information
# and shall use it only in accordance with the terms of the license agreement you
# entered into with Galbot, Inc.
#
# UNAUTHORIZED COPYING, USE, OR DISTRIBUTION OF THIS SOFTWARE, OR ANY PORTION OR
# DERIVATIVE THEREOF, IS STRICTLY PROHIBITED. IF YOU HAVE RECEIVED THIS SOFTWARE IN
# ERROR, PLEASE NOTIFY GALBOT, INC. IMMEDIATELY AND DELETE IT FROM YOUR SYSTEM.
#####################################################################################
#          _____             _   _       _   _
#         / ____|           | | | |     | \ | |
#        | (___  _   _ _ __ | |_| |__   |  \| | _____   ____ _
#         \___ \| | | | '_ \| __| '_ \  | . ` |/ _ \ \ / / _` |
#         ____) | |_| | | | | |_| | | | | |\  | (_) \ V / (_| |
#        |_____/ \__, |_| |_|\__|_| |_| |_| \_|\___/ \_/ \__,_|
#                 __/ |
#                |___/
#
#####################################################################################
#
# Description: Add a mesh to the scene
# Author: Chenyu Cao@Galbot
# Date: 2025-05-07
#
#####################################################################################

from physics_simulator import PhysicsSimulator
from synthnova_config import PhysicsSimulatorConfig, RobotConfig, MeshConfig
from pathlib import Path


def main():
    # Create sim config
    my_config = PhysicsSimulatorConfig()

    # Initialize the simulator
    synthnova_physics_simulator = PhysicsSimulator(my_config)

    # Add default scene
    synthnova_physics_simulator.add_default_scene()

    # Add robot
    robot_config = RobotConfig(
        prim_path="/World/Galbot",
        name="galbot_one_charlie",
        mjcf_path=Path()
            .joinpath(synthnova_physics_simulator.synthnova_assets_directory)
            .joinpath("synthnova_assets")
            .joinpath("robot")
            .joinpath("galbot_one_charlie_description")
            .joinpath("galbot_one_charlie.xml"),
        position=[0, 0, 0],
        orientation=[0, 0, 0, 1]
    )
    synthnova_physics_simulator.add_robot(robot_config)

    # Add a shelf mesh
    shelf_config = MeshConfig(
        prim_path="/World/Shelf",
        name="shelf",
        mjcf_path=Path()
            .joinpath(synthnova_physics_simulator.synthnova_assets_directory)
            .joinpath("synthnova_assets")
            .joinpath("default_assets")
            .joinpath("example")
            .joinpath("shelf_scene")
            .joinpath("shelves")
            .joinpath("1")
            .joinpath("model")
            .joinpath("mjcf")
            .joinpath("convex_decomposition.xml"),
        position=[0.55, 0, 0],
        orientation=[0, 0, 0, 1],
        scale=[1.0, 1.0, 1.0]
    )
    synthnova_physics_simulator.add_object(shelf_config)

    # Initialize the simulator
    synthnova_physics_simulator.initialize()

    # Run the display loop
    synthnova_physics_simulator.loop()

    # Close the simulator
    synthnova_physics_simulator.close()


if __name__ == "__main__":
    main()
