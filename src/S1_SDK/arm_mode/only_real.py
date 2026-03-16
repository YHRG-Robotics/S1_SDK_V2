from S1_SDK.arm_mode.base_mode import ControlStrategy
from typing import List


class OnlyRealStrategy(ControlStrategy):
    def joint_control(self, arm, pos: List[float]) -> bool:
        if pos is not None:
            arm.motor.control_pos_vel(pos, [10.0]*len(pos))
            return True
        return False
    
    def needs_motor(self) -> bool:
        return True
    
    def needs_sim(self) -> bool:
        return False