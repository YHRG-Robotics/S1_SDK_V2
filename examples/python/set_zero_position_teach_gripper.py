import time

# 添加项目根目录到 Python 路径
from S1_SDK import S1_arm,control_mode

"""
本代码为机械臂夹爪设置零位功能，机械臂不使能，调用set_zero_position_gripper接口
将夹爪当前位置设置为夹爪零位
"""

# 初始化机械臂
# windows下使用COM+number ，linux下使用/dev/ttyUSB+number
# 例子：如windows--COM20，linux-----/dev/ttyUSB0
arm = S1_arm(control_mode.only_real,dev = "/dev/ttyCH341USB0",end_effector="teach")

time.sleep(1)

arm.set_end_zero_position()


print("set gripper to zero position.")
