from S1_SDK import Arm_Search
import sys
import glob

def find_arm_ports():
    if sys.platform.startswith('linux'):
        ports = glob.glob('/dev/ttyUSB*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/cu.usbserial*') + glob.glob('/dev/cu.usbmodem*')
    elif sys.platform.startswith('win32'):
        ports = [f'COM{i+1}' for i in range(256)]
    else:
        print(f"平台 {sys.platform} 暂不支持")
        return

    if not ports:
        print("未检测到任何串口设备")
        return

    for port in ports:
        try:
            if Arm_Search(port):
                print(f"{port} (机械臂)")
            else:
                print(f"{port} (非机械臂)")
        except Exception as e:
            print(f"尝试访问 {port} 时出错: {e}")

if __name__ == "__main__":
    find_arm_ports()