import sys
import os

# 添加项目根目录到 Python 路径
install_kdl = True
from S1_SDK.hardware.motor_interface import S1ARM,CommType,EndType,S1_Kinematics,search_arm
from S1_SDK.hardware.mujoco_sim import Mujoco
from S1_SDK.hardware.collision import CollisionChecker
# import numpy as math
from enum import IntEnum
import time 
import math
from typing import Dict,List
import S1_SDK.arm_mode as arm_mode

COM_TYPE : Dict[str,CommType] = {
    "V2":CommType.uart,
    "V1":CommType.can,
}
END_TYPE : Dict[str,EndType] = {
    "None":EndType.none,
    "gripper":EndType.gripper,
    "teach":EndType.teach,
    "mix":EndType.mix,
}
# from smotor_master import SmotorMaster
##控制模式枚举
class control_mode(IntEnum):
    only_sim = 0
    only_real = 1
    real_control_sim = 2
# 策略映射
STRATEGY_MAP: Dict[control_mode, arm_mode.ControlStrategy] = {
    control_mode.only_sim: arm_mode.OnlySimStrategy(),
    control_mode.only_real: arm_mode.OnlyRealStrategy(),
    control_mode.real_control_sim: arm_mode.RealControlSimStrategy(),
}
end_checker = ["None","gripper","teach","mix"]
range_checker = [[math.radians(-170),math.radians(170)],
                  [math.radians(0),math.radians(180)],
                  [math.radians(0),math.radians(170)],
                  [math.radians(-90),math.radians(87)],
                  [math.radians(-90),math.radians(90)],
                  [math.radians(-90),math.radians(90)],
                  [math.radians(-100),math.radians(100)],
                  ]
def clamp(value, checker):
    # for i in range(len(value)):
    if value < checker[0]:
        value = checker[0]
    elif value > checker[1]:
        value = checker[1]
    return value
class S1_arm:
    def __init__(self,mode:control_mode,dev:str="/dev/ttyUSB0",end_effector:str="None",check_collision:bool=True,arm_version:str="V2"):
        """
        初始化S1_arm类
        :param mode: 控制模式, 可选值为control_mode枚举中的值
        :param dev: 电机通信设备, 默认值为"/dev/ttyUSB0"
        :param end_effector: 末端类型, 可选值为"None","gripper","teach"
        :param check_collision: 是否检查碰撞, 默认值为True
        :param arm_version: 机械臂版本, 默认值为"V2"
        """
        if end_effector not in end_checker:
            sys.exit(f"末端执行器错误,只能为{end_checker},当前为{end_effector}")
        self.end_effector = end_effector
        self.gripper_need = False
        if end_effector != "None":
            self.gripper_need = True
        self.motor = None
        self.sim = None
        if check_collision:
            self.collision_checker = CollisionChecker(end_effector)
        else:
            self.collision_checker = None
        self.__init_arm(dev,mode,arm_version)
        if self.strategy.needs_motor():
            self.motors = 7
        else:
            self.motors = 7
        

    ###控制块###
    def joint_control_mit(self,pos = None):
        """
        MIT关节控制,控制六个关节
        :param pos: 六个关节的位置,列表形式,每个元素为一个关节的位置
        """
        if pos is None:
            return False
        if len(pos) > 6 :
            return False
        for i in range(len(pos)):
            pos[i] = clamp(pos[i],range_checker[i])
        if self.collision_checker is None:
            pass
        else:
            if self.collision_checker.check_collision(pos):
                print(f"time:{time.time()} 碰撞检测到, 控制被阻止")
                return False
        
        if self.motor is None:
            return self.strategy.joint_control(self, pos) 
        tau = self.gravity(return_tau=True)      
        return_state = self.motor.control_pos(pos[:6],tau[:6])
        return return_state

    def joint_control(self,pos = None):
        """
        关节控制,控制六个关节
        :param pos: 六个关节的位置,列表形式,每个元素为一个关节的位置
        """
        if pos is None or len(pos) > 6 or pos is None: 
            return False
        if self.collision_checker is None:
            pass
        else:
            if self.collision_checker.check_collision(pos):
                print(f"time:{time.time()} 碰撞检测到, 控制被阻止")
                return False
        return self.strategy.joint_control(self, pos[:6])       
    def control_gripper(self,pos,force):
        return self.motor.control_gripper(pos,force)
    def control_teach(self,tau):
        """
        示教控制,控制六个关节
        :param tau: 六个关节的力矩,列表形式,每个元素为一个关节的力矩
        """
        pos = self.get_pos()
        tau = tau/math.cos(math.fabs(pos[-1] + math.degrees(30))) 
        if self.get_vel()[-1]>0.5:
            tau = -tau/3
        if pos[-1] < 1.0:
            self.motor.control_teach(tau)
        else:
            self.motor.control_teach(0)
    def control_teach_zero_tau(self):
        self.motor.control_teach(0)
    def control_teach_pos(self,pos):    
        self.motor.control_teach_pos(-pos)
    def control_mix(self,pos):
        self.motor.control_mix_gripper(pos,0,5.0,0,0)
    def control_mix_zero_tau(self):
        self.motor.control_mix_gripper(0,0,0,0,0)
    def enable(self):
        """
        使能电机
        """
        if self.strategy.needs_motor():
            self.motor.enable()
    def disable(self):
        """
        失能电机
        """
        if self.strategy.needs_motor():
            self.motor.disable()

    def set_zero_position(self):
        """
        设置所有电机的零位
        """
        self.motor.set_zero_position()

    def set_end_zero_position(self):
        """
        设置末端零位
        """
        if self.strategy.needs_motor():
            self.motor.set_end_zero_position()
            # time.sleep(0.1)

    def gravity(self,return_tau=False):
        """
        :param return_tau: 是否返回重力补偿力矩,默认False
        :return: 如果return_tau为True,返回当前位置下重力补偿应输出力矩列表,否则直接控制电机
        """
        qpos = self.get_pos()
        tau = [0.0]*6
        tau  = self.motor.gravity(qpos[:6])
        if return_tau:
            return tau
        self.motor.control_foc(tau[:6])
        
    #####控制块END###

    def check_collision(self, qpos, gripper=False):
        """
        检查给定关节角度下是否发生自碰撞
        :param qpos: 关节角度列表,长度为6
        :param gripper: 是否检查夹爪,默认不带
        :return: 如果发生碰撞返回True,否则返回False
        """
        if gripper is None:
            gripper = self.gripper
        return self.collision_checker.check_collision(qpos, gripper)

    ######状态块#####
    def get_pos(self):
        """
        获取当前关节位置
        :return: 关节位置列表,每个元素为一个关节的位置
        """
        if self.strategy.needs_motor():
            return self.motor.get_position()
        elif self.strategy.needs_sim():
            return self.sim.get_pos()
    def get_vel(self):
        """
        获取当前关节速度
        :return: 关节速度列表,每个元素为一个关节的速度
        """
        if self.strategy.needs_motor():
            return self.motor.get_velocity()
        else:
            return [0.0]*self.motors
    def get_tau(self):
        """
        获取当前关节力矩
        :return: 关节力矩列表,每个元素为一个关节的力矩
        """
        if self.strategy.needs_motor():
            return self.motor.get_torque()
        else:
            return [0.0]*6
    def get_temp(self):
        """
        获取当前关节温度
        :return: 关节温度列表,每个元素为一个关节的温度
        """
        if self.strategy.needs_motor():
            return self.motor.get_coil_temperature()
        else:
            return [0.0]*self.motors
    #####状态块END###
        
    def close(self):
        """
        关闭电机
        """
        if self.strategy.needs_motor():
            self.disable()
    def __init_arm(self,dev,mode,arm_version):
        self.strategy = STRATEGY_MAP.get(mode)
        if not self.strategy:
            raise ValueError(f"模式错误(mode error){mode}")
        if self.strategy.needs_motor():
            self.motor = S1ARM(dev,COM_TYPE[arm_version],END_TYPE[self.end_effector])
        if self.strategy.needs_sim():
            script_dir = os.path.dirname(os.path.abspath(__file__))
            if self.end_effector == "None":
                self.sim = Mujoco(os.path.join(script_dir,'resource/gripper_less.xml'))
            elif self.end_effector == "gripper":
                self.sim = Mujoco(os.path.join(script_dir,'resource/gripper.xml'))
            elif self.end_effector == "teach":
                self.sim = Mujoco(os.path.join(script_dir,'resource/teach.xml'))
            elif self.end_effector == "mix":
                self.sim = Mujoco(os.path.join(script_dir,'resource/mix.xml'))
class S1_solver():
    def __init__(self, end_offset:List[float]) -> None:
        self.solver = S1_Kinematics(end_offset)
    def forward_quat(self, qpos:List[float]):
        """
        正解: 给定关节角度,返回末端执行器位置
        :param qpos: 关节角度列表,长度为6
        :return: 末端执行器位置列表,每个元素为一个坐标或完整位姿 [x,y,z,qx,qy,qz,qw]
        """
        return self.solver.fk_quat(qpos)
    def inverse_quat(self, pos:List[float], qpos:List[float]=None):
        """
        逆解: 给定末端执行器位置,返回关节角度
        :param pos: 末端执行器位置列表,每个元素为一个坐标或完整位姿 [x,y,z,qx,qy,qz,qw]
        :param qpos: 初始关节角度猜测,默认为零位
        :return: 关节角度列表,长度为6
        """
        if qpos is None:
            qpos = [0.0]*6
        ret = self.solver.ik_quat(pos, qpos)
        if ret == []:
            print("逆解失败")
            return None
        return ret
    def forward_euler(self, qpos:List[float]):
        """
        正解: 给定关节角度,返回末端执行器位置
        :param qpos: 关节角度列表,长度为6
        :return: 末端执行器位置列表,每个元素为一个坐标或完整位姿 [x,y,z,rx,ry,rz]
        """
        return self.solver.fk_euler(qpos)
    def inverse_euler(self, pos:List[float], qpos:List[float]=None):
        """
        逆解: 给定末端执行器位置,返回关节角度
        :param pos: 末端执行器位置列表,每个元素为一个坐标或完整位姿 [x,y,z,rx,ry,rz]
        :return: 关节角度列表,长度为6
        """
        if qpos is None:
            qpos = [0.0]*6
        ret = self.solver.ik_euler(pos, qpos)
        if ret == []:
            print("逆解失败")
            return None
        return ret
def Arm_Search(bus: str, end_effector:str="None",arm_version:str="V2") -> bool:
    """
    搜索指定总线、通信类型和末端执行器的S1臂
    :param bus: 总线名称,例如"/dev/ttyCH341USB0"
    :param end_effector: 末端执行器类型,例如"gripper","None","teach"
    :param arm_version: S1臂版本,例如"V2"
    :return: 如果找到S1臂返回True,否则返回False
    """
    return search_arm(bus, COM_TYPE[arm_version],END_TYPE[end_effector])
