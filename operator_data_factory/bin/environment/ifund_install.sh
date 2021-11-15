#!/bin/bash

cd $(dirname $0)
cd ../..
export BASE_DIR=$(pwd)

## oracle连接环境安装
mkdir -p /opt/ifund
cd /opt/ifund

# 解压包
tar -zxvf $BASE_DIR/resource/THSDataInterface_Linux_20210427.tar.gz

sudo python3 bin64/installiFinDPy.py
