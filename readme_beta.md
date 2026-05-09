### 新增接口说明
python版本
```python
def control_gripper_pos_vel(self,pos,vel):
        return self.motor.control_gripper_pos_vel(pos,vel)
def control_gripper_mit(self,pos,vel,kp,kd,tau):
    return self.motor.control_gripper_mit(pos,vel,kp,kd,tau)
```
其中pos_vel为速度位置接口，pos为目标位置，推荐范围为【0~2.0】(可为负值)
tip:小心堵转带来的电机发热风险
vel运行到目标位置的速度  

mit为达妙电机的mit接口，pos为目标位置，vel运行到目标位置的速度，kp为比例系数，kd为微分系数，tau为前馈力矩  
mit模式框图如下所示
![mit模式框图](/doc/mit.png)
目录下新增temp.py文件为使用实例
