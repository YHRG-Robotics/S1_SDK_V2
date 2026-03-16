#include "S1_SDK.hpp"
#include <memory>
#include <iostream>
#include <vector>
#include <thread>
#include <map>
#include <csignal>   
#include <atomic>    
std::atomic<bool> g_running{true};
void signal_handler(int signal) {
    if (signal == SIGINT) {
        std::cout << "\nReceived SIGINT (Ctrl+C). Shutting down gracefully..." << std::endl;
        g_running = false;  
    }
}

std::map<std::string, S1::EndEffectorType> end_type_map = {
    {"none", S1::EndEffectorType::None},
    {"gripper", S1::EndEffectorType::Gripper},
    {"teach", S1::EndEffectorType::Teach}
};

std::shared_ptr<S1::S1ARM> param_parse(int argc, char *argv[]);

int main(int argc, char *argv[]) {
    std::signal(SIGINT, signal_handler);
    std::shared_ptr<S1::S1ARM> arm;
    if ((arm = param_parse(argc, argv)) == nullptr) {
        return 1;
    }

    try {
        arm->enable(); // 使能

        while (g_running) {  
            std::vector<float> pos = arm->Get_Position();
            std::vector<float> tau = arm->Gravity(pos);
            arm->Control_Foc(tau);

            std::cout << "pos: ";
            for (auto p : pos) {
                std::cout << p << " ";
            }
            std::cout << std::endl;

            std::this_thread::sleep_for(std::chrono::milliseconds(10));
        }

        std::cout << "Disabling motors..." << std::endl;
        arm->disable();

    } catch (const std::exception& e) {
        std::cerr << "Exception: " << e.what() << std::endl;
        arm->disable();  
        return 1;
    }

    std::cout << "Shutdown complete." << std::endl;
    return 0;
}

std::shared_ptr<S1::S1ARM> param_parse(int argc, char *argv[]) {
    if (argc < 2 || argc > 3) {
        std::cerr << "Usage: " << argv[0] << " <port> [end_type]" << std::endl;
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