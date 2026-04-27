import argparse
from S1_SDK import control_mode

MODE_MAP = {
    "only_real": control_mode.only_real,
    "only_sim": control_mode.only_sim,
}

def create_parser(description: str, include_mode: bool = True, default_dev: str = "COM23",include_record: bool = False):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--dev", type=str, default=default_dev, help="串口设备，例如 COM23 或 /dev/ttyUSB0")
    if include_mode:
        parser.add_argument("--mode", type=str, choices=["only_real", "only_sim"],
                            default="only_real", help="控制模式：only_real（默认）, only_sim")
    if include_record:
        parser.add_argument("--record", type=str, default="True", help="是否记录轨迹，默认True")
    parser.add_argument("--end", type=str, default="None", help="末端执行器类型，例如 'gripper', 'None' ,'teach', 'mix' 等")
    return parser
