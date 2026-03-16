#include "S1_SDK.hpp"
#include <memory>
#include <iostream>
#include <vector>
#include <thread>
#include <map>
std::map<std::string,S1::EndEffectorType> end_type_map = {
    {"none",S1::EndEffectorType::None},
    {"gripper",S1::EndEffectorType::Gripper},
    {"teach",S1::EndEffectorType::Teach}
};

std::shared_ptr<S1::S1ARM> param_parse(int argc, char *argv[]);//参数解析
int main(int argc, char *argv[])
{
    std::shared_ptr<S1::S1ARM> arm;//创建指针
    if((arm = param_parse(argc,argv)) == nullptr)
    {
        return 0;
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
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