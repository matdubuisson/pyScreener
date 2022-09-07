#!/bin/bash

bash linux_get_permissions_pyScreener.bash

if [[ "$1" != "--with-executables" ]]; then
    bash linux_check_tools_pyScreener.bash
    bash linux_update_executables_pyScreener.bash
fi

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

cd $current_path

# Copy logo in /etc/pyScreener/
sudo mkdir $path
sudo cp linux/logo_pyScreener.png "$path."

# Copy linux_exectubles in /etc/pyScreener/
sudo cp linux/client_gui_pyScreener "$path."

# Copy f.desktop in /usr/share/applications/
sudo cp linux/$desktop_file_name "$desktop_file_addr."
