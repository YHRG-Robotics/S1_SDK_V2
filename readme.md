# S1机械臂SDK V2

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)]()

S1机械臂SDK提供了控制机械臂运动、读取状态、执行正逆运动学等功能的Python API。开发者可以轻松实现关节控制、末端控制、示教、碰撞检测等功能。

---

## 目录

- [功能特性](#功能特性)
- [系统要求](#系统要求)
- [安装指南](#安装指南)
- [快速开始](#快速开始)
- [C++接口说明](#c-接口说明)
- [核心功能](#核心功能)
  - [初始化与控制模式](#初始化与控制模式)
  - [状态读取](#状态读取)
  - [运动控制](#运动控制)
  - [运动学求解](#运动学求解)
  - [高级功能](#高级功能)
- [示例代码](#示例代码)
- [API参考](#api参考)
- [常见问题](#常见问题)

---

## 功能特性

- **关节控制**：关节位置/力矩控制、MIT模式控制
- **末端控制**：笛卡尔空间位姿控制（正向/逆向运动学）
- **运动学求解**：基于KDL的正解/逆解（支持四元数、欧拉角）
- **示教与回放**：轨迹记录与复现
- **碰撞检测**：自碰撞检测与安全保护
- **夹爪控制**：末端执行器力矩/位置控制
- **重力补偿**：动态重力补偿功能
- **状态监控**：实时读取位置、速度、力矩、温度
- **多模式支持**：实机/仿真/混合模式

---

## 系统要求

| 平台 | 支持状态 | 版本 |
|------|----------|------|
| Linux | ✅ 完全支持 | Ubuntu 18.04 / 20.04 / 22.04 |
| Windows | ✅ 支持 | Windows 10 / 11 |
| macOS | ❌ 暂不支持 | - |

**推荐平台**：Ubuntu 22.04

### 环境依赖

- Python 3.10
- conda 环境管理工具
- cmake >= 3.10
- pybind11
- C++编译工具链 (g++)

---

## 安装指南

### 1. 安装编译工具链 (Linux)

```bash
sudo apt update
sudo apt install cmake build-essential
```

### 2. 创建虚拟环境

```bash
conda create -y -n S1 python=3.10
conda activate S1
```

### 3. 克隆并安装

```bash
git clone https://github.com/YHRG-Robotics/S1_SDK_V2.git
cd S1_SDK_V2
./install.sh
```

### 4. 串口权限配置 (Linux)

```bash
sudo chmod 777 /dev/ttyUSB0
```

---

## 快速开始

SDK 提供了丰富的示例脚本，位于 `examples/python/` 目录下，所有示例都支持命令行参数，方便快速测试。

### 命令行参数说明

| 参数 | 说明 | 可选值 | 默认值 |
|------|------|--------|--------|
| `--dev` | 串口设备 | `/dev/ttyUSB0` / `COM23` | 平台相关 |
| `--mode` | 控制模式 | `only_real` / `only_sim` | `only_real` |
| `--end` | 末端执行器 | `None` / `gripper` / `teach` / `mix` | `None` |

> **串口说明**：Linux 一般为 `/dev/ttyUSB0`，Windows 一般为 `COM20` 以上。

### 常用示例

#### 1. 搜索机械臂

检测当前连接的机械臂设备：

```bash
cd examples/python
python check_arm.py
```

#### 2. 读取位置

实时读取机械臂当前关节角度：

```bash
# Linux
python read_pos.py --dev /dev/ttyUSB0 --mode only_real --end None

# Windows
python read_pos.py --dev COM23 --mode only_real
```

#### 3. 使能/失能机械臂

开启电机输出力矩：

```bash
python enable.py --dev /dev/ttyUSB0 --end gripper
```

关闭电机（释放力矩）：

```bash
python disable.py --dev /dev/ttyUSB0
```

#### 4. 键盘控制关节

使用键盘控制 6 个关节角度：

```bash
python keyboard_joint.py --dev /dev/ttyUSB0 --mode only_real --end None
```

**操作说明**：
- 数字键 `1-7`：选择关节（1=J1, 2=J2, ...）
- 方向键 ↑↓：增加/减少关节角度
- `ESC`：退出

#### 5. 重力补偿

开启重力补偿，可轻松拖动示教：

```bash
python gravity.py --dev /dev/ttyUSB0 --end None
```

> ⚠️ **安全提示**：确保机械臂平稳放置于工作空间，Ctrl+C 后机械臂会失能。

#### 6. 示教记录与回放

记录轨迹（拖动机械臂）：

```bash
python teaching.py --dev /dev/ttyUSB0 --record True
```

回放轨迹：

```bash
python teaching.py --record False
```

### 运行全部示例

```bash
cd examples/python

# 基础功能测试
python check_arm.py                    # 检测设备
python read_pos.py --dev /dev/ttyUSB0  # 读取位置
python enable.py --dev /dev/ttyUSB0    # 使能
python disable.py --dev /dev/ttyUSB0   # 失能

# 运动控制
python keyboard_joint.py --dev /dev/ttyUSB0      # 键盘控制关节
python keyboard_end_effect.py --dev /dev/ttyUSB0 # 键盘控制末端
python gravity.py --dev /dev/ttyUSB0             # 重力补偿

# 高级功能
python teaching.py --dev /dev/ttyUSB0            # 示教
python collision.py --dev /dev/ttyUSB0           # 碰撞检测
python teleop_demo.py --master_dev /dev/ttyUSB0 --slaver_dev /dev/ttyUSB1  # 遥操作
```

---

## C++ 接口说明

SDK同时提供C++接口，编译后生成可执行文件，位于 `examples/C++/` 目录下。

### 编译方法

```bash
./build.sh
```

编译完成后，可执行文件会生成在 `examples/C++/` 目录中。

### 使用方法

所有C++示例的用法一致：

```bash
./程序名 <串口设备> [末端类型]
```

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `<串口设备>` | 串口路径 | `/dev/ttyUSB0` / `COM23` |
| `[末端类型]` | 可选，末端执行器类型 | `none` / `gripper` / `teach` |

### C++ 示例程序

#### 1. 使能机械臂

```bash
./enable /dev/ttyUSB0          # 默认无末端
./enable /dev/ttyUSB0 gripper  # 使用夹爪
```

#### 2. 失能机械臂

```bash
./disable /dev/ttyUSB0
```

#### 3. 读取位置

实时循环读取关节角度：

```bash
./read_pos /dev/ttyUSB0
```

输出格式：`pos: 0.1 0.2 0.0 0.0 0.0 0.0 0.0`

#### 4. 位置速度控制

运行周期性位置控制示例：

```bash
./control_pos_vel /dev/ttyUSB0
```

#### 5. 重力补偿

开启重力补偿，Ctrl+C退出：

```bash
./gravity /dev/ttyUSB0
```

#### 6. 设置零位

```bash
./set_zero_pos /dev/ttyUSB0       # 设置机械臂零位
./set_end_zero_pos /dev/ttyUSB0   # 设置末端执行器零位
```

### C++ API 参考

#### S1ARM 类

```cpp
#include "S1_SDK.hpp"

// 初始化
S1::S1ARM arm(port, S1::CommType::Uart, S1::EndEffectorType::None);

// 基本控制
arm.enable();                           // 使能
arm.disable();                          // 失能
arm.Set_Zero_Position();               // 设置零位
arm.Set_End_Zero_Position();           // 设置末端零位

// 运动控制
arm.Control_Pos_Vel(pos, vel);         // 位置速度控制
arm.Control_Pos(pos, tau);             // 位置力矩控制
arm.Control_Foc(tau);                  // 纯力矩控制
arm.Control_Gripper(pos, tau);         // 夹爪控制
arm.Control_Teach(tau);                // 示教控制
arm.Control_Mix(pos);            // 控制复合式夹爪


// 状态读取
std::vector<float> pos = arm.Get_Position();
std::vector<float> vel = arm.Get_Velocity();
std::vector<float> tau = arm.Get_Torque();
std::vector<float> temp_coil = arm.Get_Coil_Temperature();
std::vector<float> temp_mos = arm.Get_Mos_Temperature();

// 重力补偿
std::vector<float> gravity_torque = arm.Gravity(position);
```

#### S1_Kinematics 类

```cpp
#include "S1_SDK.hpp"

// 初始化，传入末端偏移量
std::vector<float> offset = {0.0, 0.0, 0.0};
S1::S1_Kinematics kin(offset);

// 正解
std::vector<float> pose_quat = kin.Fk_Quat(joint_positions);    // 四元数
std::vector<float> pose_euler = kin.Fk_Euler(joint_positions);  // 欧拉角

// 逆解
std::vector<float> joints = kin.Ik_Quat(target_pose_quat);
std::vector<float> joints = kin.Ik_Euler(target_pose_euler);
```

#### 枚举类型

```cpp
// 通信类型
S1::CommType::Can   // CAN总线 (S1 V1)
S1::CommType::Uart  // UART (S1 V2)

// 末端执行器类型
S1::EndEffectorType::None
S1::EndEffectorType::Gripper
S1::EndEffectorType::Teach
S1::EndEffectorType::Mix
```

#### 辅助函数

```cpp
// 搜索机械臂
bool found = S1::Search_Arm(port, S1::CommType::Uart, S1::EndEffectorType::None);
```

---

## 核心功能

### 初始化与控制模式

#### 构造函数

```python
S1_arm(
    mode: control_mode,           # 控制模式
    dev: str = "/dev/ttyUSB0",    # 串口设备
    end_effector: str = "None",   # 末端类型
    check_collision: bool = True, # 碰撞检测开关
    arm_version: str = "V2"       # 硬件版本
)
```

#### 控制模式

| 模式 | 枚举值 | 说明 |
|------|--------|------|
| 仅仿真 | `control_mode.only_sim` | MuJoCo仿真环境，安全验证 |
| 仅实机 | `control_mode.only_real` | 控制真实机械臂 |
| 混合模式 | `control_mode.real_control_sim` | 实机与数字孪生联动 |

#### 末端执行器类型

| 类型 | 说明 |
|------|------|
| `"None"` | 无末端执行器 |
| `"gripper"` | 夹爪 |
| `"teach"` | 示教器 |
| `"mix"` | 复合式夹爪 |

---

### 状态读取

```python
# 获取关节位置（弧度）
position = arm.get_pos()  # 返回: [j1, j2, j3, j4, j5, j6, j7]

# 获取关节速度
velocity = arm.get_vel()

# 获取关节力矩
torque = arm.get_tau()

# 获取电机温度
temp = arm.get_temp()
```

> **注意**：状态读取仅在实机模式下有效，仿真模式返回默认值。

---

### 运动控制

#### 关节位置控制

```python
# 标准关节控制
target_pos = [0.5, 0.0, 0.0, 0.0, 0.0, 0.0]
arm.joint_control(target_pos)

# MIT模式（响应更快）
arm.joint_control_mit(target_pos)
```

#### 关节限位范围

| 关节 | 最小值 | 最大值 |
|------|--------|--------| 
| J1 | -170° | 170° |      
| J2 | 0° | 180° |
| J3 | 0° | 170° |
| J4 | -90° | 87° |
| J5 | -90° | 90° |
| J6 | -90° | 90° |
| J7 | -100° | 100° |

SDK会自动对超出范围的角度进行裁剪。

#### 末端执行器控制

```python
# 夹爪控制
arm.control_gripper(pos=1.0, force=0.5)
arm.control_mix(pos = 0.5)
# pos: 位置范围 0~2.0
# force: 力矩限制
```

---

### 运动学求解
#### 求解器使用

```python
from S1_SDK import S1_solver

# 初始化求解器，传入末端偏移量（单位：米）
solver = S1_solver([0.0, 0.0, 0.0])

# 正向运动学：关节角度 -> 末端位姿
joint_angles = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

# 四元数格式 [x, y, z, qx, qy, qz, qw]
pose_quat = solver.forward_quat(joint_angles)

# 欧拉角格式 [x, y, z, rx, ry, rz]
pose_euler = solver.forward_euler(joint_angles)

# 逆向运动学：末端位姿 -> 关节角度
target = [0.2, 0.0, 0.3, 0.0, 0.0, 0.0, 1.0]
joints = solver.inverse_quat(target)
# 或
joints = solver.inverse_euler([0.2, 0.0, 0.3, 0.0, 0.0, 0.0])

if joints:
    arm.joint_control(joints)
else:
    print("逆解失败：目标不可达")
```

---

### 高级功能

#### 使能与失能

```python
arm.enable()   # 使能电机，准备运动
arm.disable()  # 失能电机，释放力矩
```

> ⚠️ **安全提示**：失能后机械臂会失去支撑，请确保处于安全位置。

#### 零位设置

```python
# 设置机械臂零位（需在物理零位标记处执行）
arm.set_zero_position()

# 设置末端执行器零位
arm.set_end_zero_position()
```

> ⚠️ **注意**：设置零位时需对准机械臂本体上的零位标记，错误的零位设置可能导致危险。

#### 重力补偿

```python
# 开启重力补偿模式
arm.gravity()

# 或获取补偿力矩而不控制
gravity_torque = arm.gravity(return_tau=True)
```

#### 碰撞检测

```python
# 检查指定角度是否会发生碰撞
is_collision = arm.check_collision([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

# 初始化时关闭碰撞检测
arm = S1_arm(mode=control_mode.only_real, check_collision=False)
```

#### 机械臂搜索

```python
from S1_SDK import Arm_Search

# 搜索指定端口的机械臂
found = Arm_Search("/dev/ttyUSB0", end_effector="gripper")
if found:
    print("机械臂已连接")
```

---

## 示例代码

### 示例1：关节空间运动

```python
from S1_SDK import S1_arm, control_mode
import time

# 初始化
arm = S1_arm(
    mode=control_mode.only_real,
    dev="/dev/ttyUSB0",
    end_effector="None",
    check_collision=True
)

# 使能
arm.enable()

# 依次运动到几个位置
positions = [
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.5, 0.5, 0.5, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
]

for pos in positions:
    arm.joint_control(pos)
    time.sleep(1.0)

# 失能
arm.disable()
```

### 示例2：笛卡尔空间运动

```python
from S1_SDK import S1_arm, S1_solver, control_mode

arm = S1_arm(control_mode.only_real, dev="/dev/ttyUSB0")
solver = S1_solver([0.0, 0.0, 0.0])

arm.enable()

# 目标位置：x=0.3, y=0.0, z=0.2, 姿态直立
target_pose = [0.3, 0.0, 0.2, 0.0, 0.0, 0.0, 1.0]

# 逆解计算
joints = solver.inverse_quat(target_pose)

if joints:
    # 验证正解
    pose = solver.forward_quat(joints)
    print(f"目标: {target_pose}")
    print(f"正解: {pose}")
    
    # 执行运动
    arm.joint_control(joints)
else:
    print("目标不可达")

arm.disable()
```

### 示例3：轨迹记录与回放

```python
from S1_SDK import S1_arm, control_mode
import time

arm = S1_arm(control_mode.only_real, dev="/dev/ttyUSB0")
arm.enable()

print("开始记录轨迹...")
trajectory = []
try:
    for _ in range(200):  # 记录10秒
        pos = arm.get_pos()
        trajectory.append(pos)
        time.sleep(0.05)
except KeyboardInterrupt:
    pass

print(f"记录完成，共{len(trajectory)}个点")
print("开始回放...")

for pos in trajectory:
    arm.joint_control(pos)
    time.sleep(0.05)

print("回放完成")
arm.disable()
```

---

## API参考

### S1_arm 类

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `__init__` | mode, dev, end_effector, check_collision, arm_version | - | 初始化 |
| `enable` | - | - | 使能电机 |
| `disable` | - | - | 失能电机 |
| `joint_control` | pos: List[float] | bool | 关节位置控制 |
| `joint_control_mit` | pos: List[float] | bool | MIT关节控制 |
| `control_gripper` | pos: float, force: float | - | 夹爪控制 |
| `control_teach` | tau: float | - | 示教控制 |
| `get_pos` | - | List[float] | 获取关节位置 |
| `get_vel` | - | List[float] | 获取关节速度 |
| `get_tau` | - | List[float] | 获取关节力矩 |
| `get_temp` | - | List[float] | 获取电机温度 |
| `set_zero_position` | - | - | 设置机械臂零位 |
| `set_end_zero_position` | - | - | 设置末端零位 |
| `gravity` | return_tau: bool | List[float] \| None | 重力补偿 |
| `check_collision` | qpos: List[float] | bool | 碰撞检测 |
| `close` | - | - | 关闭连接 |

### S1_solver 类

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `forward_quat` | qpos: List[float] | List[float] | 正解（四元数） |
| `inverse_quat` | pos: List[float] | List[float] \| None | 逆解（四元数） |
| `forward_euler` | qpos: List[float] | List[float] | 正解（欧拉角） |
| `inverse_euler` | pos: List[float] | List[float] \| None | 逆解（欧拉角） |

### 辅助函数

| 函数 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `Arm_Search` | bus, end_effector, arm_version | bool | 搜索机械臂 |

### 常量

```python
# 控制模式
control_mode.only_sim          # 仅仿真
control_mode.only_real         # 仅实机
control_mode.real_control_sim  # 混合模式

# 通信类型
COM_TYPE["V2"]  # UART - S1 V2
COM_TYPE["V1"]  # CAN - S1 V1

# 末端执行器
END_TYPE["None"]     # 无
END_TYPE["gripper"]  # 夹爪
END_TYPE["teach"]    # 示教器
```

---

## 常见问题

### Q1: 串口权限错误

```
Permission denied: '/dev/ttyUSB0'
```

**解决**：
```bash
sudo chmod 777 /dev/ttyUSB0
```

Windows用户需安装CH340驱动。

### Q2: 机械臂无法使能

**检查**：
1. 串口是否正确连接
2. 电源是否开启
3. 通信协议版本是否正确（V1/V2）
4. 末端执行器类型是否匹配

### Q3: 逆解失败/返回None

**原因**：
- 目标位置超出工作空间
- 目标姿态无法到达

**建议**：先使用正解验证可达空间。

### Q4: 碰撞检测阻止运动

**解决**：
```python
# 临时关闭碰撞检测
arm = S1_arm(..., check_collision=False)
```

### Q5: 夹爪无法响应

**检查**：
- 初始化时是否正确指定 `end_effector="gripper"`
- 位置参数是否在有效范围（0~2.0）

### Q6: 运动不连贯/抖动

**建议**：
- 使用 `joint_control_mit` 获得更平滑的运动
- 降低控制频率或增加插值点
- 检查通信稳定性

### Q7: 温度读取异常

**说明**：温度读取仅在实机模式下有效，仿真模式返回全零。

---

## 项目结构

```
S1_SDK_V2/
├── src/                    # SDK源代码
│   ├── S1_SDK/            # Python核心模块
│   │   ├── S1_arm.py      # 主控制类
│   │   ├── arm_mode/      # 控制模式
│   │   ├── hardware/      # 硬件接口
│   │   └── resource/      # 模型资源
│   └── S1_SDK_C++/        # C++示例
├── examples/              # 示例程序
│   └── python/           # Python示例
├── include/              # C++头文件
├── doc/                  # 文档
└── images/               # 图片资源
```

---

## 许可

MIT License

## 技术支持

如有问题，请访问：[GitHub Issues](https://github.com/YHRG-Robotics/S1_SDK_V2/issues)

---

**注意**：使用机械臂时请务必注意安全，远离运动区域，避免碰撞和挤压。
