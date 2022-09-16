#!/bin/bash

path="../installer/linux/"

if [[ ! -d linux ]]; then
    mkdir linux
fi

cd ../app/
pyinstaller --onefile client_gui_pyScreener.py
mv dist/client_gui_pyScreener $path
