import sys, termios, tty, time,select
from S1_SDK import S1_arm, control_mode

# 初始化机械臂
arm = S1_arm(
    mode=control_mode.only_real,
    dev="/dev/ttyCH341USB0",
    end_effector="gripper",
    arm_version="V2"
)
arm.enable()

deta = 0.1
pos = 0.0
print("使用键盘控制 gripper: w/s 增减, q 退出")

# 保存终端原始设置
fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)

# 设置 raw 模式
tty.setraw(fd)
last_pos = 0.0
last_pos = 0.0
def gripper_control(tar_pos: float, spd: float):
    tar_tau = 1.5
    max_tau = 0.2
    global last_pos, last_spd
    tar_pos = max(0.0, min(2.0, tar_pos))
    now_pos = arm.get_pos()[-1]
    delta_pos = (now_pos - tar_pos) * tar_tau
    if delta_pos>max_tau:
        delta_pos = max_tau
    elif delta_pos<-max_tau:
        delta_pos = -max_tau
    arm.control_end_effector(-tar_pos, 0.0, 0.5, 0.1, delta_pos)
def clamp(x, min_val, max_val):
    return max(min_val, min(x, max_val))
def gripper_control(tar_pos: float, spd: float):
    current_position = arm.get_pos()[-1]
    current_velocity = arm.get_vel()[-1]
    home_position = 1.4
    x = -current_position
    v = current_velocity
    
    x0 = -home_position
    Ks = 0.25
    B  = 0.01
    Ka = 0.02
    tau = Ks * (x0 - x) + B * v

    if (v > 0.1):
        tau += Ka * abs(v)
    

    tau = clamp(tau, -2.0, 2.0)

    arm.control_end_effector(0, 0.0, 0.0, 0.0, tau)
    # acc = spd - last_spdq
    # print(f"delta_pos: {delta_pos:.2f}, tar_pos: {tar_pos:.2f}", end="\n\r", flush=True)
    # if  delta_pos > 0.1 and spd < 0.1:
    #     arm.control_end_effector(0, 0.0, 0.0, 1.0, 0.5)
    #     print(f"堵转")
    # else:
    # # print(f"gripper pos: {tar_pos:.2f}")
        
    #     arm.control_end_effector(-tar_pos, 0.0, 5.0, 1.0, 0.0)
    # last_pos = tar_pos
    # last_spd = spd

try:
    while True:
        # 非阻塞读取单字符
        if select.select([sys.stdin], [], [], 0.01)[0]:
            ch = sys.stdin.read(1)
            if ch == 'w':
                pos += deta
                # print(f"pos: {pos:.2f}")
            elif ch == 's':
                pos -= deta
                # print(f"pos: {pos:.2f}")
            elif ch == 'e':
                pos = 0.0
                # print(f"pos: {pos:.2f}")
            elif ch == 'q':
                pos = 2.0
                # print(f"pos: {pos:.2f}")
            elif ch == 'c':
                break
        spd = arm.get_vel()
        # print("\033[2J\033[H", end="")  # 清屏 + 光标移动到左上角
        # print(f"spd: {spd[-1]:.2f}", end="\n\r", flush=True)
        gripper_control(pos,spd[-1])
        time.sleep(0.005)
except KeyboardInterrupt:
    pass
finally:
    # 恢复终端
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    arm.disable()
    print("\n机械臂已停止")