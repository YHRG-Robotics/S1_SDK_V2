import time
from S1_SDK import S1_arm, control_mode
from common import create_parser

"""
本代码为测试机械臂自碰撞检测功能。
机械臂不使能运动控制（仅重力补偿），调用 joint_control 接口，
此时机械臂不会主动运动，可以手动拖动。
当机械臂与自身发生碰撞时，终端会打印警告信息。
"""

def main():
    parser = create_parser("S1 机械臂自碰撞检测测试脚本", include_mode=False)
    args = parser.parse_args()

    # 创建机械臂实例
    arm = S1_arm(
        mode=control_mode.real_control_sim,
        dev=args.dev,
        end_effector=args.end
    )

    try:
        arm.enable()
        print(f"机械臂已使能，设备: {args.dev}, 末端: {args.end}")
        current_pos = [0.0] * 6

        while True:
            arm.gravity()  
            current_pos = arm.get_pos()
            arm.joint_control(current_pos[:6])  
            time.sleep(0.001)

    except KeyboardInterrupt:
        print("\n检测到 Ctrl+C，机械臂失能中...")
    finally:
        arm.close()
        print("机械臂已失能，安全退出。")

if __name__ == "__main__":
    main()