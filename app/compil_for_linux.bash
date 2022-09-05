#!/bin/bas
h
echo "Please, the compilation needs super user permisions :"
sudo echo "Done !!" || (echo "Can't compil pyScreener without permisions sorry..." ; exit 0)
echo "========================================================="

sudo pyinstaller --onefile client_gui_pyScreener.py
sudo mv dist/* ../installer/executables/linux/
