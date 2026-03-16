#ifndef S1_ARM_HPP
#define S1_ARM_HPP
#include <memory>      // for std::unique_ptr
#include <string>
#include <vector>
namespace S1{
enum class CommType {
    Can,
    Uart
};
enum class EndEffectorType {
    None,
    Gripper,
    Teach
};
class S1ARM{
public:
    S1ARM(std::string bus,CommType comm,EndEffectorType end_effect);
    ~S1ARM();
    // uint8_t close();
    uint8_t enable();
    uint8_t disable();
    uint8_t Control_Pos_Vel(std::vector<float>& pos, std::vector<float>& vel);
    uint8_t Control_Pos(std::vector<float>& pos, std::vector<float>& tau);
    uint8_t Control_Foc(std::vector<float>& tau);
    void Control_Teach(float tau);
    void  Control_Gripper(float pos, float tau);
    // uint8_t Control_MIT(std::vector<float>& pos, std::vector<float>& vel, std::vector<float>& kp, std::vector<float>& kd,std::vector<float>& tau);
    void Set_Zero_Position();
    void Set_End_Zero_Position();

    std::vector<float> Get_Position();
    std::vector<float> Get_Velocity();
    std::vector<float> Get_Torque();
    std::vector<float> Get_Coil_Temperature();
    std::vector<float> Get_Mos_Temperature();

    std::vector<float> Gravity(std::vector<float>& position);
private:
    class Impl; 
    std::unique_ptr<Impl> pimpl_;
};
class S1_Kinematics{
public:
    S1_Kinematics(std::vector<float> end_effector_offset);
    ~S1_Kinematics();
    std::vector<float> Ik_Quat(std::vector<float>& target_pose);
    std::vector<float> Ik_Euler(std::vector<float>& target_pose);
    std::vector<float> Fk_Quat(std::vector<float>& joint_positions);
    std::vector<float> Fk_Euler(std::vector<float>& joint_positions);
private:
    class Impl; 
    std::unique_ptr<Impl> pimpl_;
};
bool Search_Arm(std::string bus, CommType comm, EndEffectorType end_effect);
}
#endif
