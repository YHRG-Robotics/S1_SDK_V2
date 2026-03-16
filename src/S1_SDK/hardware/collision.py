import mujoco
import numpy as np
import os

class CollisionChecker:
    def __init__(self,end_effector:str="None"):
        """
        初始化时不加载具体模型，check_collision 时根据 gripper 参数加载模型。
        """
        self.model = None
        self.data = None
        self.joint_indices = []
        self.control_joint_names = []

        # 默认排除碰撞对（除了 'geom1','geom5' 默认检测）
        self.exclude_pairs = {
            ('geom11', 'geom6'),
            ('geom7', 'geom9'),
            ('geom10', 'geom6'),
            ('geom0', 'geom1'),
            ('geom11', 'geom9'),
            ('geom11', 'geom7'),
            ('geom6', 'geom8'),
            ('geom10', 'geom9'),
            ('geom11', 'geom8'),
            ('geom6', 'geom9'),
            ('geom10', 'geom8'),
            ('geom1', 'geom9'),
            ('geom2', 'geom9'),
            ('geom2', 'geom8'),
            ('geom1', 'geom8'),
            ('geom0', 'geom9'),
            ('geom2', 'geom5'),
            # ('geom0', 'geom10'),
        }
        
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        if end_effector == "None":
            self.model  = self._load_model(gripper=False)
        else:
            self.model  = self._load_model(gripper=True)

    def _load_model(self, gripper=True):
        """
        根据 gripper 参数加载对应模型
        """
        if gripper:
            xml_path = os.path.join(self.script_dir, "../resource/meshes/gripper.xml")
        else:
            xml_path = os.path.join(
                os.path.dirname(__file__),  # 当前文件目录：S1_SDK/hardware/
                "../resource/meshes/gripper_less.xml"  # 正确相对路径
            )

        if not os.path.exists(xml_path):
            raise FileNotFoundError(f"XML 文件未找到: {xml_path}")

        self.model = mujoco.MjModel.from_xml_path(xml_path)
        self.data = mujoco.MjData(self.model)

        # 自动选择非自由关节
        self.joint_indices = [
            i for i in range(self.model.njnt)
            if self.model.jnt_type[i] != mujoco.mjtJoint.mjJNT_FREE
        ]
        self.control_joint_names = [self.model.joint(i).name for i in self.joint_indices]

    def check_collision(self, qpos, gripper=True):
        """
        检查给定关节角度下是否发生自碰撞
        :param qpos: 至少 6 个关节角度数组
        :param gripper: True 使用带夹爪模型, False 使用无夹爪模型
        :return: (bool, set) 是否碰撞, 碰撞对
        """
        # 如果还没加载模型，则加载对应模型
        if self.model is None:
            self._load_model(gripper)

        # 只取前 6 个关节
        qpos = qpos[:6]

        qpos[3] = qpos[3] + 0.01

        if gripper and len(qpos) >= 3:
            if -0.01 <= qpos[2] <= 0.01:
                qpos[2] = 0.0   # 自动吸附为 0
            if -0.01 <= qpos[3] <= 0.01:
                qpos[3] = 0.0   # 自动吸附为 0
            # 确保关节3的角度在 0~0.02 范围内

        # 更新关节角度
        n_joints_to_use = min(len(qpos), len(self.joint_indices))
        for idx in range(n_joints_to_use):
            jnt_id = self.joint_indices[idx]
            self.data.qpos[jnt_id] = qpos[idx]

        mujoco.mj_forward(self.model, self.data)
        mujoco.mj_step(self.model, self.data)

        # ---------------- 动态处理 geom1-geom5 ----------------
        exclude_pairs = set(self.exclude_pairs)
        if gripper and len(qpos) >= 3:
            q3 = qpos[2]  # 关节3
            q4 = qpos[3]  # 关节4

            if not (0 <= q3 <= 0.02) or q4 < -0.02:
                # 关节3不在 0~0.01 时排除 ('geom1','geom5')
                exclude_pairs.add(('geom1', 'geom5'))
            else:
                # 在 0~0.02 时保持检测，不排除
                exclude_pairs.discard(('geom1', 'geom5'))
        # -------------------------------------------------------

        collision_pairs = set()
        for i in range(self.data.ncon):
            contact = self.data.contact[i]

            geom1_name = self.model.geom(contact.geom1).name or f"geom{contact.geom1}"
            geom2_name = self.model.geom(contact.geom2).name or f"geom{contact.geom2}"
            if geom1_name == "floor" or geom2_name == "floor":
                continue
            elif geom1_name == "geom2" or geom2_name == "geom5":
                continue
            elif geom1_name == "geom0" or geom2_name == "geom10":
                continue
            print(geom1_name, geom2_name)
            body1_name = self.model.body(self.model.geom_bodyid[contact.geom1]).name
            body2_name = self.model.body(self.model.geom_bodyid[contact.geom2]).name
            pair_geom = tuple(sorted([geom1_name, geom2_name]))
            pair_full = (
                f"{geom1_name} (link={body1_name})",
                f"{geom2_name} (link={body2_name})"
            )

            if pair_geom not in exclude_pairs:
                collision_pairs.add(pair_full)

        return (len(collision_pairs) > 0)



if __name__ == "__main__":
    checker = CollisionChecker()

    # 测试带夹爪
    q_test = [0, 0, 0.000001, 0, 0, 0] 
    has_collision, pairs = checker.check_collision(q_test, gripper=True)
    if has_collision:
        print("⚠️ 带夹爪碰撞:")
        for p in pairs:
            print("   ", p)
    else:
        print("✅ 带夹爪无碰撞")
