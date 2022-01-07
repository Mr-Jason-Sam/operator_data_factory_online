#!/bin/bash

cd $(dirname $0)
cd ../..
BASE_DIR=$(pwd)

cd $BASE_DIR/tools/ifund

sudo python3 bin64/installiFinDPy.py
