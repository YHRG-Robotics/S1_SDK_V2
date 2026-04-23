

include(CMakeFindDependencyMacro)

# 查找依赖
find_dependency(Threads)

# 导入目标
if(NOT TARGET S1_SDK::motor_core)
    include("${CMAKE_CURRENT_LIST_DIR}/S1_SDKTargets.cmake")
endif()
