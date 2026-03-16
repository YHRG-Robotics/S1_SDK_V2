import os
import math
from pynput import keyboard
from S1_SDK import S1_arm,control_mode
import time
import argparse
"""
本代码为机械臂笛卡尔空间控制，使用键盘控制末端
注意:
    1. 调用end_effector_control接口使机械臂末端效应器根据键盘输入进行移动
    2. 按下空格，末端开始向上运动，WSAD控制末端前后左右移动
    3. 由于逆解的多解和无解特征，在某些姿态下（尤其与坐标原点较近情况下），关节可能解算到会突变的位置，使用者应远离机械臂的工作空间
"""
position = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]
deta = 0.02
now_joint = 0

# 初始化机械臂
# windows下使用COM+number ，linux下使用/dev/ttyUSB+number
# 例子：如windows--COM20，linux-----/dev/ttyUSB0
# arm = S1_arm(control_mode.only_real,dev="COM23",end_effector="None")
# arm.enable()
# arm.enable()
current_pos = [0.0] * 6
delta = 0.005  # 每次调整 1 度（转为弧度）
MODE_MAP = {
    "only_real": control_mode.only_real,
    "only_sim": control_mode.only_sim,
}
def on_press(key):
    global now_joint
    try:
        print(f'按下了: {key.char}')
        if key.char == '1':
            now_joint = 0
        elif key.char == '2':
            now_joint = 1
        elif key.char == '3':
            now_joint = 2
        elif key.char == '4':
            now_joint = 3
        elif key.char == '5':
            now_joint = 4
        elif key.char == '6':
            now_joint = 5
        elif key.char == '7':
            now_joint = 6
    except AttributeError:
        if key == keyboard.Key.up:
            position[now_joint] += deta
        elif key == keyboard.Key.down:
            position[now_joint] -= deta
        print(f'按下了特殊键: {key}')
def on_release(key):
    if key == keyboard.Key.esc:
        print("退出监听...")
        return False  # 停止监听
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
def main():
    try:
        parser = argparse.ArgumentParser(description="S1 机械臂关节角度控制脚本")
        parser.add_argument("--dev", type=str, default="COM23", help="串口设备，例如 COM23 或 /dev/ttyUSB0")
        parser.add_argument("--mode", type=str, choices=["only_real", "only_sim"],
                            default="only_real", help="控制模式：only_real（默认）, sim_and_real, only_sim")
        parser.add_argument("--end", type=str, default="None", help="末端执行器类型，例如 'gripper', 'None' ,'teach'")

        args = parser.parse_args()
        arm = S1_arm(
            mode=MODE_MAP[args.mode],
            dev=args.dev,
            end_effector=args.end
        )
        arm.enable()
        while True:
            # print(f"pos: {[f'{p:8.3f}' for p in position]}")
            arm.joint_control(position[:6])
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("程序手动中断")
        arm.close()
        listener.stop()

if __name__ == "__main__":
        main()