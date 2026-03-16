import os
import sys
# 添加项目根目录到 Python 路径
from S1_SDK import S1_arm,control_mode
import time
import csv
import argparse

"""
本代码为机械臂示教功能，带参数启动时，为记录模式，使用者拖动机械臂进行运动  如 python3 teaching.py 1
不带参数启动时，为播放模式，读取CSV文件中的位置数据，机械臂根据数据进行运动 如 python3 teaching.py
将机械臂当前位置记录到CSV文件中
"""

output_path = os.path.dirname(os.path.abspath(__file__))
header_written = False
parser = argparse.ArgumentParser(description="S1 机械臂记录轨迹脚本")
parser.add_argument("--dev", type=str, default="COM23", help="串口设备，例如 COM23 或 /dev/ttyUSB0")
parser.add_argument("--end", type=str, default="None", help="末端执行器类型，例如 'gripper', 'None' ,'teach'")
parser.add_argument("--record", type=bool, default=True, help="是否记录轨迹，默认True")
args = parser.parse_args()
def load_csv_data(file_path):
    """读取记录的CSV文件，返回位置数据列表"""
    data = []
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # 跳过标题行
            for row in reader:
                positions = list(map(float, row[1:7]))  # row[0]是时间戳
                data.append(positions)
        return data
    except FileNotFoundError:
        print(f"错误：未找到记录文件 {file_path}")
        return None
    except Exception as e:
        print(f"读取文件失败：{e}")
        return None
    
def save_frame_to_csv(frame_data):
    """将一帧数据保存到 CSV 文件"""
    global header_written
    
    row = frame_data if isinstance(frame_data, (list, tuple)) else list(frame_data.values())
    csv_path = os.path.join(output_path, "data.csv")
    with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        if not header_written:
            header = ['time', '1','2','3','4','5','6',
                     '1','2','3','4','5','6',
                     '1','2','3','4','5','6']  # leader_left
            writer.writerow(header)
            header_written = True

        writer.writerow(row)

def initialize_motors():
    """初始化电机和控制器"""
    motors = None
    motors = S1_arm(control_mode.only_real,dev=args.dev,end_effector=args.end)
    motors.enable()
    return motors

def record_mode(motors):
    """记录模式主循环"""
    try:
        now_position = [0.0] * 6
        now_torgue = [0.0] * 6
        
        while True:
            now_position = motors.get_pos()
            motors.gravity()
            save_frame_to_csv([time.time(), *now_position, *now_torgue])
            time.sleep(0.005)
            
    except KeyboardInterrupt:
        motors.close()
        sys.exit(0)

def replay_mode(motors,csv_path):
    """复现模式主循环"""
    recorded_positions = load_csv_data(csv_path)
    if not recorded_positions:
        print("无有效记录数据，程序退出")
        sys.exit(1)
    # 启用电机并设置零点
    

    try:
        index = 0
        
        while True:
            if index >= len(recorded_positions):
                index = 0  # 循环复现

            target_pos = recorded_positions[index]
            # for i in range(len(motors)):
            tempture = motors.get_temp()
            print(tempture,end="\r")
            # print(f"tempture: {[f'{p:.3f}' for p in tempture]}",end="\r")
            motors.joint_control_mit(target_pos)
                # pass
            index += 1
            
            time.sleep(0.005)
            
    except KeyboardInterrupt:
        # for i in range(len(motors)):
        motors.close()
        # motors.close()
        print("\n退出程序")
def replay_mode_wave(motors,csv_path):
    """复现模式主循环"""
    recorded_positions = load_csv_data(csv_path)
    if not recorded_positions:
        print("无有效记录数据，程序退出")
        sys.exit(1)
    # 启用电机并设置零点
    
    target_pos = [0.0] * 4
    try:
        index = [0,50,100,150]
        target_pos = [0.0] * 4
        for i in range(len(motors)):
            target_pos[i] = recorded_positions[index[i]]
            motors[i].joint_control(target_pos[i])
        time.sleep(5)
        # print(len(recorded_positions))
        while True:
            for i in range(len(motors)):
                index[i] += 1
                if index[i] >= len(recorded_positions):
                    index[i] = 0  # 循环复现
            for i in range(len(motors)):
                target_pos[i] = recorded_positions[index[i]]
            
            for i in range(len(motors)):
                motors[i].joint_control_mit(target_pos[i])
                pass
            # index += 1
            
            time.sleep(0.005)
            
    except KeyboardInterrupt:
        for i in range(len(motors)):
            motors[i].close()
        # motors.close()
        print("\n退出程序")

if __name__ == "__main__":
    if args.record:
        print("进入记录模式...")
        motors= initialize_motors()
        csv_path = os.path.join(output_path, "data.csv")
        if os.path.exists(csv_path):
            os.remove(csv_path)
        time.sleep(1)
        record_mode(motors)
        print("开始录制...")
    else:
        print("进入复现模式...")
        motors= initialize_motors()
        # motors.enable()
        time.sleep(1)
        csv_path = os.path.join(output_path, "data.csv")
        if not os.path.exists(csv_path):
            print(f"⚠️ 警告: 文件不存在: {csv_path}")
            sys.exit(1)  # 非 0 退出表示异常
        replay_mode(motors,csv_path)