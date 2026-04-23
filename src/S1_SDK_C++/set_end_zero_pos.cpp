#include "S1_SDK.hpp"
#include <memory>
#include <iostream>
#include <vector>
#include <thread>
#include "common.hpp"

int main(int argc, char *argv[])
{
    std::shared_ptr<S1::S1ARM> arm;//创建指针
    if((arm = param_parse(argc,argv)) == nullptr)
    {
        return 0;
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    arm->Set_End_Zero_Position();
}