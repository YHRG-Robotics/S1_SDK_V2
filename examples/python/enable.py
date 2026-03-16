import time
from S1_SDK import S1_arm,control_mode
import argparse
"""
本代码为机械臂使能功能,调用enable接口
注意:
    1. 调用enable接口使机械臂开始输出力矩,使用者需注意自身与设备的安全，防止设备发生碰撞
    2. 机械臂的运动需要先使能，才能控制，此时注意控制指令，避免使用者和设备发生危险
"""

# 初始化机械臂
# windows下使用COM+number ，linux下使用/dev/ttyUSB+number
# 例子：如windows--COM20，linux-----/dev/ttyUSB0

def main():
    parser = argparse.ArgumentParser(description="S1 机械臂笛卡尔空间控制脚本")
    parser.add_argument("--dev", type=str, default="COM23", help="串口设备，例如 COM23 或 /dev/ttyUSB0")
    parser.add_argument("--end", type=str, default="None", help="末端执行器类型，例如 'gripper', 'None' ,'teach'")

    args = parser.parse_args()
    arm = S1_arm(
        mode=control_mode.only_real,
        dev=args.dev,
        end_effector=args.end
    )
    # arm = S1_arm(control_mode.only_sim,dev="COM20",end_effector="gripper")
    arm.enable()
    print("enable")
if __name__ == "__main__":
    main()
