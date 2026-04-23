import os
import math
from pynput import keyboard
from S1_SDK import S1_arm,control_mode,S1_solver
import time
from common import create_parser, MODE_MAP
"""
本代码为机械臂笛卡尔空间控制，使用键盘控制末端
注意:
    1. 调用end_effector_control接口使机械臂末端效应器根据键盘输入进行移动
    2. 按下空格，末端开始向上运动，WSAD控制末端前后左右移动
    3. 由于逆解的多解和无解特征，在某些姿态下（尤其与坐标原点较近情况下），关节可能解算到会突变的位置，使用者应远离机械臂的工作空间
"""
# position = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]
position = [-0.018,0.0,0.219,0,0.0,0]
deta = 0.001

# 初始化机械臂
# windows下使用COM+number ，linux下使用/dev/ttyUSB+number
# 例子：如windows--COM20，linux-----/dev/ttyUSB0
current_pos = [0.08,0.0,0.20,0.0,0.0,0.0]
delta = 1  # 每次调整 1 度（转为弧度）
def on_press(key):
    try:
        # print(f'按下了: {key.char}')
        if key.char == '1':
            position[3] += deta *2
        elif key.char == '2':
            position[3] -= deta*2
        elif key.char == '3':
            position[4] += deta*2
        elif key.char == '4':
            position[4] -= deta*2
        elif key.char == '5':
            position[5] += deta*2
        elif key.char == '6':
            position[5] -= deta*2
    except AttributeError:
        if key == keyboard.Key.space:
            position[2] += deta
        elif key == keyboard.Key.shift:
            position[2] -= deta
        elif key == keyboard.Key.up:
            position[0] -= deta
        elif key == keyboard.Key.down:
            position[0] += deta
        elif key == keyboard.Key.left:
            position[1] -= deta
        elif key == keyboard.Key.right:
            position[1] += deta
        # elif key == keyboard.Key.ctrl_1:11233
            # return False  # 停止监听
        # print(f'按下了特殊键: {key}')
def on_release(key):
    if key == keyboard.Key.esc:
        print("退出监听...")
        return False  # 停止监听
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
def main():
    parser = create_parser("S1 机械臂笛卡尔空间控制脚本")
    args = parser.parse_args()
    arm = S1_arm(
        mode=MODE_MAP[args.mode],
        dev=args.dev,
        end_effector=args.end,
        check_collision=False,
    )
    solver = S1_solver(end_offset=[0.0, 0.0, 0.0])
    arm.enable()
    try:
        pos = [0.0] *6
        tar_pos = [-0.00, 0.27, 0.54,0.27, -0.00, -0.00]
        step = [0.0] *6
        for i in range(6):
            step[i] = tar_pos[i]/100
        for i in range(100):
            for j in range(6):
                pos[j] = pos[j] + step[j]
            arm.joint_control_mit(pos)
            time.sleep(0.01)
        
        
        while True:
            current_pos = arm.get_pos()
            pos = solver.inverse_euler(position,current_pos)
            
            arm.joint_control_mit(pos)
            # fk_pos = solver.forward_euler(pos)
            # print(f"当前位置: {fk_pos[0]:.2f}, {fk_pos[1]:.2f}, {fk_pos[2]:.2f}")
            time.sleep(0.005)
    except KeyboardInterrupt:
        print("\n退出程序")
        arm.close()
        

if __name__ == "__main__":
    
    main()
