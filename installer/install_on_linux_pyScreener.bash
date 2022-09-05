#!/bin/bash

echo "Some installations can be done as python3, pip, pyinstaller and tkinter !!"
echo "Please, the installer needs super user permisions :"
sudo echo "Done !!" || (echo "Can't install pyScreener without permisions sorry..." ; exit 0)
echo "========================================================="

echo "Check for the python tools :"
sudo apt-get update
echo "Installation with apt-get :"
sudo apt-get install -y python3 python3-pip python3-tk
echo "Installation with pip of python3 :"
sudo python3 -m pip install pyinstaller

current_path=`pwd`
path="/etc/pyScreener/"
if [[ -d $path ]]; then
    sudo rm -R $path
fi
desktop_file_name="pyScreener.desktop"
desktop_file_addr="/usr/share/applications/"
desktop_file="$desktop_file_addr$desktop_file_name"
if [[ -f $desktop_file ]]; then
    sudo rm $desktop_file
fi
sudo mkdir $path
sudo cp tools/logo_pyScreener.png "$path."

cd ../app/
sudo pyinstaller --onefile client_gui_pyScreener.py
sudo mv dist/client_gui_pyScreener "$path."
cd $current_path
sudo cp tools/$desktop_file_name "$desktop_file_addr."
