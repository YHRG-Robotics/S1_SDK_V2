import sys, termios, tty, time,select
# from S1_SDK import S1_solver
from S1_SDK import S1_arm,control_mode
arm = S1_arm(control_mode.only_real,dev = "/dev/ttyUSB0",end_effector="mix")
arm.enable()
while True:
    pos = arm.get_pos()
    print(pos)    
    arm.control_mix(pos[-1])
    
    time.sleep(0.1)
