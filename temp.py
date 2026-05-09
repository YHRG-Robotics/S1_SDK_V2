from S1_SDK import S1_arm,control_mode
import time

arm = S1_arm(dev="/dev/ttyUSB0",mode=control_mode.only_real,end_effector="gripper")
arm.enable()
try:
    while True:
        time.sleep(1)
        # arm.control_gripper_mit(0.5,0,5,0,0)
        # arm.control_gripper_pos_vel(0.5,5)
except KeyboardInterrupt:
    arm.disable()
