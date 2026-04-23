#include "S1_SDK.hpp"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
/********************************pybind11 interface************************************/
namespace py = pybind11;
PYBIND11_MODULE(motor_interface, m) {
    py::enum_<S1::CommType>(m, "CommType")
            .value("uart", S1::CommType::Uart)
            .value("can", S1::CommType::Can)
            .export_values();  // 允许直接用 comm_type.CAN

    py::enum_<S1::EndEffectorType>(m, "EndType")
        .value("gripper", S1::EndEffectorType::Gripper)
        .value("teach", S1::EndEffectorType::Teach)
        .value("none", S1::EndEffectorType::None)
        .value("mix", S1::EndEffectorType::Mix)
        .export_values();
    py::class_<S1::S1ARM>(m, "S1ARM")
        .def(py::init<std::string,S1::CommType,S1::EndEffectorType>())           // 构造函数
        .def("enable", &S1::S1ARM::enable)
        .def("disable", &S1::S1ARM::disable)
        .def("control_pos_vel", &S1::S1ARM::Control_Pos_Vel)
        .def("control_pos", &S1::S1ARM::Control_Pos)
        .def("control_foc", &S1::S1ARM::Control_Foc)
        .def("get_position", &S1::S1ARM::Get_Position)
        .def("get_velocity", &S1::S1ARM::Get_Velocity)
        .def("get_torque", &S1::S1ARM::Get_Torque)
        .def("get_coil_temperature", &S1::S1ARM::Get_Coil_Temperature)
        .def("get_mos_temperature", &S1::S1ARM::Get_Mos_Temperature)
        .def("control_teach", &S1::S1ARM::Control_Teach)
        .def("control_teach_pos", &S1::S1ARM::Control_Teach_Pos)
        .def("control_gripper", &S1::S1ARM::Control_Gripper)
        .def("control_mix_gripper", &S1::S1ARM::Control_Mix_Gripper)
        .def("set_zero_position", &S1::S1ARM::Set_Zero_Position)
        .def("set_end_zero_position", &S1::S1ARM::Set_End_Zero_Position)
        .def("gravity", &S1::S1ARM::Gravity);
    py::class_<S1::S1_Kinematics>(m, "S1_Kinematics")
        .def(py::init<std::vector<float>>())
        .def("ik_quat", &S1::S1_Kinematics::Ik_Quat)
        .def("ik_euler", &S1::S1_Kinematics::Ik_Euler)
        .def("fk_quat", &S1::S1_Kinematics::Fk_Quat)
        .def("fk_euler", &S1::S1_Kinematics::Fk_Euler);
    m.def("search_arm", &S1::Search_Arm);
};