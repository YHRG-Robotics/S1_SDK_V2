import time
import math
from S1_SDK import S1_arm,control_mode
import argparse
"""
本代码为测试机械臂读取当前位置功能，机械臂不使能，调用get_pos接口
此时机械臂不会运动，终端会打印当前位置，采用弧度制
"""

# 初始化机械臂
# windows下使用COM+number ，linux下使用/dev/ttyUSB+number
# 例子：如windows--COM20，linux-----/dev/ttyUSB0
MODE_MAP = {
    "only_real": control_mode.only_real,
    "only_sim": control_mode.only_sim,
}
def main():
    parser = argparse.ArgumentParser(description="S1 机械臂读角度测试脚本")
    parser.add_argument("--dev", type=str, default="COM23", help="串口设备，例如 COM23 或 /dev/ttyUSB0")
    parser.add_argument("--mode", type=str, choices=["only_real", "only_sim"],
                        default="only_real", help="控制模式：only_real（默认）, sim_and_real, only_sim")
    parser.add_argument("--end", type=str, default="None", help="末端执行器类型，例如 'gripper', 'None' ,'teach'")

    args = parser.parse_args()
    arm = S1_arm(
        mode=MODE_MAP[args.mode],
        dev=args.dev,
        end_effector=args.end,
        arm_version="V2"
    )
    current_pos = [0.0] * 7
    arm.disable()
    try:
        while True:
            current_pos = arm.get_pos()
            print(f"pos: {[f'{p:8.3f}' for p in current_pos]}")
            time.sleep(0.01)
    except KeyboardInterrupt:
        arm.close()
        print("\n退出程序")
if __name__ == "__main__":
    main()