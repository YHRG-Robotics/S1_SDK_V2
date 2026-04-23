#ifndef S1_COMMON_HPP
#define S1_COMMON_HPP

#include "S1_SDK.hpp"
#include <memory>
#include <iostream>
#include <map>
#include <string>

inline std::map<std::string, S1::EndEffectorType> end_type_map = {
    {"none", S1::EndEffectorType::None},
    {"gripper", S1::EndEffectorType::Gripper},
    {"teach", S1::EndEffectorType::Teach}
};

inline std::shared_ptr<S1::S1ARM> param_parse(int argc, char *argv[]) {
    if (argc < 2 || argc > 3) {
        std::cerr << "Usage: " << argv[0] << " <port>(such as /dev/ttyUSB0) [end_type]" << std::endl;
        std::cerr << "  end_type: none (default), gripper, teach" << std::endl;
        return nullptr;
    }

    try {
        if (argc == 2) {
            return std::make_shared<S1::S1ARM>(argv[1], S1::CommType::Uart, S1::EndEffectorType::None);
        } else {
            auto it = end_type_map.find(argv[2]);
            if (it != end_type_map.end()) {
                return std::make_shared<S1::S1ARM>(argv[1], S1::CommType::Uart, it->second);
            } else {
                std::cerr << "Invalid end type: " << argv[2] << std::endl;
                std::cerr << "Choose from: none, gripper, teach" << std::endl;
                return nullptr;
            }
        }
    } catch (const std::exception& e) {
        std::cerr << "Failed to initialize arm: " << e.what() << std::endl;
        return nullptr;
    }
}

#endif // S1_COMMON_HPP
