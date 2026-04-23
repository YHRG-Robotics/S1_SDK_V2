import time

# 添加项目根目录到 Python 路径
from S1_SDK import S1_arm,control_mode
from common import create_parser

"""
本代码为机械臂重力补偿功能,调用gravity接口
注意:
    1. 调用gravity接口使机械臂在重力作用下保持平衡,可以轻松拖动示教
    2. 此时机械臂需要平稳安置于工作空间,此时机械臂为力矩控制，若机械臂不是平稳放置，机械臂输出力矩与方向无法保证，极易发生危险
    3. Ctrl+C 后机械臂会失能，注意防止坠落
"""

# 初始化机械臂
# windows下使用COM+number ，linux下使用/dev/ttyUSB+number
# 例子：如windows--COM20，linux-----/dev/ttyUSB0
# arm = S1_arm(control_mode.only_real,dev="COM11",end_effector="gripper")
# current_pos = [0.0] * 6
# arm.enable()


def main():
    try:
        parser = create_parser("S1 机械臂重力补偿脚本", include_mode=False)
        args = parser.parse_args()
        print(f"使用串口: {args.dev}, 末端执行器: {args.end}")
        arm = S1_arm(
            mode=control_mode.only_real,
            dev=args.dev,
            end_effector=args.end
        )
        arm.enable()
        # 重力补偿
        while True:
            arm.gravity()
            time.sleep(0.005)   
    except KeyboardInterrupt:
        print("\n检测到 Ctrl+C,机械臂失能中...")
        time.sleep(0.1)
        arm.disable()
        print("机械臂已失能，安全退出。")
if __name__ == "__main__":
    main()
