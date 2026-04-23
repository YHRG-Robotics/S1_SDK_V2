#include "S1_SDK.hpp"
#include <memory>
#include <iostream>
#include <vector>
#include <thread>
#include <csignal>      // for signal handling
#include <atomic>       // for std::atomic<bool>
#include "common.hpp"

static std::atomic<bool> g_should_exit{false};
std::vector<float> make_pos();
void signal_handler(int signal);
int main(int argc, char *argv[])
{
    std::signal(SIGINT,  signal_handler);
    std::signal(SIGTERM, signal_handler);
    std::shared_ptr<S1::S1ARM> arm;//创建指针
    if((arm = param_parse(argc,argv)) == nullptr)
    {
        return 0;
    }
    arm->enable(); //使能
    std::vector<float> vel = {10,10,10,10,10,10};
    std::cout << "Control loop started. Press Ctrl+C to stop.\n";
    while(!g_should_exit)
    {
        std::vector<float> pos = arm->Get_Position();//获取当前位置
        // std::cout << "pos: " ;
        // for(auto p:pos)
        // {
        //     std::cout << p << " ";
        // }
        // std::cout << std::endl;
        std::vector<float> tar_pos = make_pos();//生成目标位置
        arm->Control_Pos_Vel(tar_pos,vel);//控制位置和速度
        std::this_thread::sleep_for(std::chrono::milliseconds(2));
    }
    arm->disable();
}

std::vector<float> make_pos(){
    static float local_tick = 0;
    static float direction = 1;
    if(local_tick > 0.75)
    {
        direction = -1;
    }
    else if(local_tick <= 0)
    {
        direction = 1;
    }
    local_tick += 0.0001 * direction;
    std::vector<float> joint_pos = {0,local_tick,local_tick,0,0,0};   
    return joint_pos;
}
void signal_handler(int signal) {
    if (signal == SIGINT || signal == SIGTERM) {
        std::cout << "\n\nReceived signal " << signal 
                  << ". Shutting down\n";
        g_should_exit = true;
    }
}