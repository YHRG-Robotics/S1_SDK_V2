#include "S1_SDK.hpp"
#include <memory>
#include <iostream>
#include <vector>
#include <thread>
#include <map>
#include <csignal>      // for signal handling
#include <atomic>       // for std::atomic<bool>
std::map<std::string,S1::EndEffectorType> end_type_map = {
    {"none",S1::EndEffectorType::None},
    {"gripper",S1::EndEffectorType::Gripper},
    {"teach",S1::EndEffectorType::Teach}
};
static std::atomic<bool> g_should_exit{false};
std::vector<float> make_pos();
void signal_handler(int signal);
std::shared_ptr<S1::S1ARM> param_parse(int argc, char *argv[]);//参数解析
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

std::shared_ptr<S1::S1ARM> param_parse(int argc, char *argv[])
{
    if(argc < 2 || argc > 3)
    {
        std::cerr << "Usage: " << argv[0] << " <port>(such as /dev/ttyUSB0)" <<" <end type(in none, gripper, teach)>"<< std::endl;
        return nullptr;
    }
    std::shared_ptr<S1::S1ARM> arm;
    try{
        
        switch(argc)
        {
            case 2:
                arm = std::make_shared<S1::S1ARM>(argv[1],S1::CommType::Uart,S1::EndEffectorType::None);
                break;
            case 3:
                if (end_type_map.find(argv[2]) != end_type_map.end())
                {
                    arm = std::make_shared<S1::S1ARM>(argv[1],S1::CommType::Uart,end_type_map[argv[2]]);
                }
                else
                {
                    std::cerr << "Usage: " << argv[0] << " <port>(such as /dev/ttyUSB0)" <<" <end type(in none, gripper, teach)>"<< std::endl;
                    return nullptr;
                }
                break;
        }
    }
    catch(const std::exception& e)
    {
        std::cerr << e.what() << '\n';
        return nullptr;
    }
    return arm;
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