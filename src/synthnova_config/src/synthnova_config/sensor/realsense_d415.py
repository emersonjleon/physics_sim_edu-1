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
# Description: Sensor config for Realsense D415 RGB and Depth camera
# Author: Herman Ye@Galbot
# Date: 2025-03-06
#
#####################################################################################


from .basic import RgbSensorConfig, DepthSensorConfig
from typing import Literal, List, Optional


class RealsenseD415RgbSensorConfig(RgbSensorConfig):
    """
    Configuration class for the RealSense D415 RGB camera.

    Intrinsics of "Color" / 1280x720 / {YUYV/RGB8/BGR8/RGBA8/BGRA8/Y16}:
      - Width:         1280
      - Height:        720
      - PPX:           629.409301757812
      - PPY:           366.805267333984
      - Fx:            912.569580078125
      - Fy:            909.815246582031
      - Distortion:    Inverse Brown Conrady (using plumb_bob model)
      - Coeffs:        [0.0, 0.0, 0.0, 0.0, 0.0]
      - FOV (deg):     70.08 x 43.17
    """

    frequency: float | None = 60.0
    width: int | None = 1280
    height: int | None = 720
    fx: float | None = 912.569580078125
    fy: float | None = 909.815246582031
    cx: float | None = 629.409301757812
    cy: float | None = 366.805267333984
    pixel_size: float | None = 0.003
    f_stop: float | None = 0.0
    focus_distance: float | None = 0.0
    projection_type: str | None = "pinhole"
    clipping_range: list[float] | None = [0.05, 15.0]
    distortion_model: str | None = "plumb_bob"
    distortion_coefficients: list[float] | None = [0.0, 0.0, 0.0, 0.0, 0.0]
    horizontal_fov: float | None = 70.08
    vertical_fov: float | None = 43.17


class RealsenseD415DepthSensorConfig(DepthSensorConfig):
    """
    Configuration class for the RealSense D415 Depth camera.

    Intrinsics of "Depth" / 1280x720 / {Z16}:
      - Width:         1280
      - Height:        720
      - PPX:          631.942749023438
      - PPY:          363.001342773438
      - Fx:           890.299133300781
      - Fy:           890.299133300781
      - Distortion:   Brown Conrady (using plumb_bob model)
      - Coeffs:       [0.0, 0.0, 0.0, 0.0, 0.0]
      - FOV (deg):    71.42 x 44.03
    """

    frequency: int = 60
    width: int = 1280
    height: int = 720
    fx: float = 890.299133300781
    fy: float = 890.299133300781
    cx: float = 631.942749023438
    cy: float = 363.001342773438
    pixel_size: float = 0.003
    f_stop: float = 0.0
    focus_distance: float = 0.0
    projection_type: Literal["pinhole"] = "pinhole"
    clipping_range: List[float] = [0.05, 15.0]
    distortion_model: Literal["plumb_bob"] = "plumb_bob"
    distortion_coefficients: List[float] = [0.0, 0.0, 0.0, 0.0, 0.0]
    horizontal_fov: float = 71.42
    vertical_fov: float = 44.03
