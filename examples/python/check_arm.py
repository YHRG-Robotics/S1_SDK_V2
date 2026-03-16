import serial.tools.list_ports
import sys
from S1_SDK import S1_arm,control_mode

ports = serial.tools.list_ports.comports()
ports_dictory = {}
if not ports:
    print("未检测到任何串口设备。")
else:
    print("检测到的串口设备：")
    for port in ports:
        print(port.device, port.description)
        if sys.platform.startswith('win'):
            if "USB-SERIAL CH340" in port.description:
                ports_dictory[port.device] = port.description
        if sys.platform.startswith('linux'):
            if "USB Serial" in port.description:
                ports_dictory[port.device] = port.description
if ports_dictory == {}:
    sys.exit("未检测到任何串口设备。")
for key, value in ports_dictory.items():
    try:
        # print(f"{key}","(尝试连接)")
        arm = S1_arm(control_mode.only_real,dev=key,end_effector="None")
        print(f"{key}","(机械臂)")
        arm.close()
    except:
        print(f"{key}","(非机械臂)")
        