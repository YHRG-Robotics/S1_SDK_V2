from abc import ABC, abstractmethod
from typing import List
class ControlStrategy(ABC):
    """控制策略抽象基类"""
    @abstractmethod
    def joint_control(self, arm, pos: List[float]) -> bool:
        pass
    

    
    @abstractmethod
    def needs_motor(self) -> bool:
        pass
    
    @abstractmethod
    def needs_sim(self) -> bool:
        pass