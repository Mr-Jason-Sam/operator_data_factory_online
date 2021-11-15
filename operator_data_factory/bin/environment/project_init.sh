#!/bin/bash

cd $(dirname $0)
export BASE_DIR=$(pwd)

## 顺序不能乱

# 环境准备
# sudo sh $BASE_DIR/python3_install.sh
sudo sh $BASE_DIR/oracle_install.sh
sudo sh $BASE_DIR/ifund_install.sh

cd ../..
# 依赖包安装
pip3 install --no-index --find-links=pkg/ -r requirements.txt

sh bin/start.sh
