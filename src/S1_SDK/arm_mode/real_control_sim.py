from S1_SDK.arm_mode.base_mode import ControlStrategy
from typing import List
import threading
import time

class RealControlSimStrategy(ControlStrategy):
    def __init__(self):
        self.arm = None
        self._stop_event = threading.Event()
        self.refresh_thread = threading.Thread(target=self._refresh_loop)
        self.refresh_thread.daemon = True  
        self.refresh_thread.start()
        self.target_pos = None

    def joint_control(self, arm, pos: List[float]) -> bool:
        if self.arm is None:
            self.arm = arm
            return False
        self.target_pos = pos
        return True
    def _refresh_loop(self):
        while not self._stop_event.is_set():
            if self.arm is not None:
                self.arm.sim.refresh()
                if self.target_pos is not None:
                    self.arm.sim.control(self.target_pos)
            time.sleep(0.01)  # 100 Hz
    
    def needs_motor(self) -> bool:
        return True
    
    def needs_sim(self) -> bool:
        return True
