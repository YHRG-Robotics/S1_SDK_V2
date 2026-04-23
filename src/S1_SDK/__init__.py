# hardware/__init__.py

# from .smotor_master import SmotorMaster
from .S1_arm import  S1_arm,control_mode,S1_solver,Arm_Search
__all__ = ['control_mode', 'S1_arm','S1_solver','Arm_Search']
