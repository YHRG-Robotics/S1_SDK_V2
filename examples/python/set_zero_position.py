import time
from S1_SDK import S1_arm,control_mode
from common import create_parser
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
    parser = create_parser("S1 机械臂设置零位脚本", include_mode=False)
    args = parser.parse_args()
    arm = S1_arm(
        mode=control_mode.only_real,
        dev=args.dev,
        end_effector=args.end
    )
    # arm = S1_arm(control_mode.only_sim,dev="COM20",end_effector="gripper")
    arm.set_zero_position()
    print("set to zero position")
if __name__ == "__main__":
    main()
