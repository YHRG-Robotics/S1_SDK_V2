import mujoco
import mujoco.viewer
import math
class Mujoco:
    def __init__(self,PATH): 
        "mujoco仿真类"
        self.MODEL_XML_PATH = PATH
        self.model = mujoco.MjModel.from_xml_path(self.MODEL_XML_PATH)
        self.data = mujoco.MjData(self.model)
        self.viewer =  mujoco.viewer.launch_passive(self.model, self.data,show_right_ui=False,show_left_ui=False)  
        lenght  = len(self.data.qpos)
        if lenght == 5:
            self.data_len = 5
        else:
            self.data_len = 6
        self.pos = [0.0]*self.data_len

    def refresh(self):
        self.viewer.sync()
        self.pos = self.data.qpos[:self.data_len]
    def control(self,positon):
        for i in range(self.data_len):
                self.data.qpos[i] = positon[i]
        if self.data_len == 6 and len(positon) > 6:
            print(len(self.data.qpos))
            self.data.qpos[6] = (positon[6]/2.1)*0.05
            self.data.qpos[7] = -(positon[6]/2.1)*0.05
        mujoco.mj_forward(self.model, self.data)
    def close(self):
        self.viewer.close()
    def get_pos(self):
        return self.pos