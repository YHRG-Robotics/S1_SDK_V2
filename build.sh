#!/bin/bash
get_arch=$(uname -m)
echo $get_arch
case $get_arch in
    "x86_64")
        echo "x86_64"
        ;;
    "arm64")
        echo "arm64"
        ;;
    *)
        echo "unknown arch"
        ;;
esac
mkdir -p build
cd build
if [ $get_arch == "arm64" ]; then
    cmake -DIS_ARM=ON ..
else
    cmake ..
fi
make -j$(nproc)
pip install -e .