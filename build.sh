#!/bin/bash
set -e

get_arch=$(uname -m)
echo "------------------------------------------"
echo "Architecture: $get_arch"
echo "Python: $(which python3)"
echo "------------------------------------------"

PYBIND_PATH=$(python3 -c "import pybind11; print(pybind11.get_cmake_dir())" 2>/dev/null || echo "")

if [ -z "$PYBIND_PATH" ]; then
    echo "当前 Python 环境未安装 pybind11。"
    exit 1
fi

if [ -d "build" ]; then
    rm -rf build
fi
mkdir -p build
cd build

if [ "$get_arch" == "aarch64" ]; then
    cmake -DIS_ARM=ON -Dpybind11_DIR="$PYBIND_PATH" ..
else
    cmake -Dpybind11_DIR="$PYBIND_PATH" ..
fi

make -j$(nproc)

cd ..
pip install -e .