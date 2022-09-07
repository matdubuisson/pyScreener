#!/bin/bash

echo "Check for the python tools :"
sudo apt-get update
echo "Installation with apt-get :"
sudo apt-get install -y python3 python3-pip python3-tk
echo "Installation with pip of python3 :"
sudo python3 -m pip install pyinstaller


