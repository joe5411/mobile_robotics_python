import numpy as np

from mobile_robotics_python.messages import RobotStateMessage, SpeedRequestMessage
from mobile_robotics_python.tools.time import get_utc_stamp


class NaiveRotateMove:
    def __init__(self, parameters):
        self.parameters = parameters
        self.orientation_threshold = parameters["orientation_threshold"]
        self.rotation_speed = parameters["rotation_speed"]
        self.linear_speed = parameters["linear_speed"]

    def sign(self, value):
        if value == 0:
            return 1
        elif value < 0:
            return -1
        elif value > 0:
            return 1

    def compute_request(
        self, current_position: RobotStateMessage, desired_position: RobotStateMessage
    ) -> SpeedRequestMessage:

        print(
            current_position.x_m,
            current_position.y_m,
            desired_position.x_m,
            desired_position.y_m,
        )
        diff_x = desired_position.x_m - current_position.x_m
        diff_y = desired_position.y_m - current_position.y_m
        desired_theta = np.arctan2(diff_y, diff_x)
        diff_theta = desired_theta - current_position.yaw_rad
        distance = (diff_x**2 + diff_y**2) ** 0.5
        print(
            "Desired theta:",
            desired_theta,
            "diff_theta",
            diff_theta,
            "distance:",
            distance,
        )
        msg = SpeedRequestMessage()
        msg.stamp_s = get_utc_stamp()
        msg.vx_mps = 0
        msg.wz_radps = 0
        if abs(diff_theta) > self.orientation_threshold:
            msg.wz_radps = self.rotation_speed * np.sign(diff_theta)
            print("inside rotating loop", msg.wz_radps)
            return msg

        if distance > 0:
            sign = 1
            # if abs(diff_x) > abs(diff_y):
            #    sign = self.sign(diff_x)
            # else:
            #    sign = self.sign(diff_y)
            msg.vx_mps = self.linear_speed * sign
            print("inside distance loop", msg.vx_mps)
            return msg
        return msg
