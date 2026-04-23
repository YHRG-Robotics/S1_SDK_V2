cmake_minimum_required(VERSION 3.10)
project(S1_C++)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 目录定义
set(OUTPUT_DIR_HARDWARE ${CMAKE_SOURCE_DIR}/src/S1_SDK/hardware)
set(CPP_BIN_DIR         ${CMAKE_SOURCE_DIR}/examples/C++)
set(MOTOR_CORE_INCLUDE  ${CMAKE_SOURCE_DIR}/include)

option(IS_ARM "is arm arch" OFF)
option(BUILD_PYTHON "Build Python extension module" ON)
option(BUILD_EXAMPLES "Build C++ examples" ON)

find_package(Threads REQUIRED)

# --- 平台适配逻辑 ---
if(WIN32)
    set(MOTOR_CORE_LIB ${CMAKE_SOURCE_DIR}/lib/windows/lib/motor_core.lib)
elseif(APPLE)
    # macOS 适配：区分 M系列芯片 (arm64) 和 Intel (x86_64)
    if(CMAKE_SYSTEM_PROCESSOR STREQUAL "arm64")
        set(MOTOR_CORE_LIB ${CMAKE_SOURCE_DIR}/lib/macos/arm64/libmotor_core.a)
    else()
        set(MOTOR_CORE_LIB ${CMAKE_SOURCE_DIR}/lib/macos/x86_64/libmotor_core.a)
    endif()
    
    # 串口通信需要链接 macOS 的原生框架
    find_library(IOKIT_LIB IOKit REQUIRED)
    find_library(CF_LIB CoreFoundation REQUIRED)
    set(PLATFORM_LIBS ${IOKIT_LIB} ${CF_LIB})
elseif(UNIX AND NOT APPLE)
    if(IS_ARM OR CMAKE_SYSTEM_PROCESSOR MATCHES "aarch64")
        set(MOTOR_CORE_LIB ${CMAKE_SOURCE_DIR}/lib/linux/aarch64/libmotor_core.a)
    else()
        set(MOTOR_CORE_LIB ${CMAKE_SOURCE_DIR}/lib/linux/x86_64/libmotor_core.a)
    endif()
else()
    message(FATAL_ERROR "Unsupported platform")
endif()

# 校验库是否存在
if(NOT EXISTS ${MOTOR_CORE_LIB})
    message(WARNING "Library not found: ${MOTOR_CORE_LIB}")
endif()

# --- 构建 Python 模块 ---
if(BUILD_PYTHON)
    find_package(pybind11 REQUIRED)
    pybind11_add_module(motor_interface MODULE src/S1_interface.cpp)
    # 链接核心库、线程库及 macOS 框架
    target_link_libraries(motor_interface PRIVATE ${MOTOR_CORE_LIB} Threads::Threads ${PLATFORM_LIBS})
    target_include_directories(motor_interface PRIVATE ${MOTOR_CORE_INCLUDE})
    set_target_properties(motor_interface PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY ${OUTPUT_DIR_HARDWARE}
        PREFIX ""
    )
endif()

# --- 构建 C++ 示例 ---
if(BUILD_EXAMPLES)
    set(EXAMPLES
        "read_pos"          "src/S1_SDK_C++/read_pos.cpp"
        "control_pos_vel"   "src/S1_SDK_C++/control_pos_vel.cpp"
        "disable"           "src/S1_SDK_C++/disable.cpp"
        "enable"            "src/S1_SDK_C++/enable.cpp" 
        "set_zero_pos"      "src/S1_SDK_C++/set_zero_pos.cpp"
        "set_end_zero_pos"  "src/S1_SDK_C++/set_end_zero_pos.cpp"
        "gravity"           "src/S1_SDK_C++/gravity.cpp"
    )

    while(EXAMPLES)
        list(GET EXAMPLES 0 EXE_NAME)
        list(GET EXAMPLES 1 SRC_PATH)
        
        add_executable(${EXE_NAME} ${SRC_PATH})
        # 同样链接 macOS 框架
        target_link_libraries(${EXE_NAME} PRIVATE ${MOTOR_CORE_LIB} Threads::Threads ${PLATFORM_LIBS})
        target_include_directories(${EXE_NAME} PRIVATE ${MOTOR_CORE_INCLUDE})
        set_target_properties(${EXE_NAME} PROPERTIES
            RUNTIME_OUTPUT_DIRECTORY ${CPP_BIN_DIR}
        )
        
        list(REMOVE_AT EXAMPLES 0 1)
    endwhile()
endif()