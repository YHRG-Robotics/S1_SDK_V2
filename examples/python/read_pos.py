import time
import math
from S1_SDK import S1_arm,control_mode
from common import create_parser, MODE_MAP
"""
本代码为测试机械臂读取当前位置功能，机械臂不使能，调用get_pos接口
此时机械臂不会运动，终端会打印当前位置，采用弧度制
"""

# 初始化机械臂
# windows下使用COM+number ，linux下使用/dev/ttyUSB+number
# 例子：如windows--COM20，linux-----/dev/ttyUSB0
def main():
    parser = create_parser("S1 机械臂读角度测试脚本")
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