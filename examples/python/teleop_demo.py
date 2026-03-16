import time
from S1_SDK import S1_arm, control_mode
import argparse
"""
本代码为主从臂遥操demo，运行代码需接入两条机械臂，一条作为主臂，一条作为从臂；
使用时注意主臂和从臂的设备接口。
"""
# windows下使用COM+number ，linux下使用/dev/ttyUSB+number
# 例子：如windows--COM20，linux-----/dev/ttyUSB0
def main():
    parser = argparse.ArgumentParser(description="S1 机械臂笛卡尔空间控制脚本")
    parser.add_argument("--master_dev", type=str, default="/dev/ttyCH341USB0", help="主臂串口设备，例如 COM23 或 /dev/ttyUSB0")
    parser.add_argument("--slaver_dev", type=str, default="/dev/ttyCH341USB1", help="从臂串口设备，例如 COM23 或 /dev/ttyUSB0")
    print("=== S1 主从臂 Teleoperation Demo ===")
    args = parser.parse_args()
    # 主臂，注意 dev 的设备接口
    master = S1_arm(control_mode.only_real, dev=args.master_dev, end_effector="teach")
    master.enable()
    # 从臂，注意 dev 的设备接口
    slave = S1_arm(control_mode.only_real, dev=args.slaver_dev, end_effector="gripper")
    slave.enable()
    print("[INFO] Teleop Started (CTRL + C to stop)")

    try:
        while True:
            master_pos = master.get_pos()
            # print("master_pos",master_pos)
            master.control_teach(0.08)
            master.gravity()
            slave.joint_control_mit(master_pos[:6])
            slave.control_gripper(master_pos[-1],0.3)
            time.sleep(0.01)  # 100Hz 循环
    except KeyboardInterrupt:
        print("\n[INFO] Teleop Stopped.")
    finally:
        master.close()
        slave.close()

if __name__ == '__main__':
    main()

