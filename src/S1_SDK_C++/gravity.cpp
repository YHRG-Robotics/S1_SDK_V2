#include "S1_SDK.hpp"
#include <memory>
#include <iostream>
#include <vector>
#include <thread>
#include <csignal>   
#include <atomic>    
#include "common.hpp"

std::atomic<bool> g_running{true};
void signal_handler(int signal) {
    if (signal == SIGINT) {
        std::cout << "\nReceived SIGINT (Ctrl+C). Shutting down gracefully..." << std::endl;
        g_running = false;  
    }
}

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