#!/bin/bash

cd $(dirname $0)
cd ../..
BASE_DIR=$(pwd)

## oracle连接环境安装
mkdir -p $BASE_DIR/tools/ifund
cd $BASE_DIR/tools/ifund

# 解压包
tar -zxvf $BASE_DIR/resource/DataInterface_free_Linux_20210812.tar.gz

# sudo python3 bin64/installiFinDPy.py
