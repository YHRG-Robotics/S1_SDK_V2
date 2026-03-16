import threading
import time
from S1_SDK.arm_mode.base_mode import ControlStrategy
from typing import List

class OnlySimStrategy(ControlStrategy):
    def __init__(self):
        self.arm = None
        self._stop_event = threading.Event()
        self.refresh_thread = threading.Thread(target=self._refresh_loop)
        self.refresh_thread.daemon = True  # 可选：设为守护线程，主程序退出时自动结束
        self.refresh_thread.start()
        self.target_pos = None

    def _refresh_loop(self):
        while not self._stop_event.is_set():
            if self.arm is not None:
                self.arm.sim.refresh()
                if self.target_pos is not None:
                    self.arm.sim.control(self.target_pos)
            time.sleep(0.01)  # 100 Hz

    def __del__(self):
        self._stop_event.set()
        self.refresh_thread.join(timeout=1)  # 避免无限阻塞

    def joint_control(self, arm, pos: List[float]) -> bool:
        if self.arm is None:
            self.arm = arm
        if pos is not None:
            self.target_pos = pos
            return True
        return False

    def needs_motor(self) -> bool:
        return False

    def needs_sim(self) -> bool:
        return True