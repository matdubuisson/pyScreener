#!/bin/bash

# Author : matdubuisson
# Source : https://github.com/matdubuisson/pyScreener
# Licence : Apache (2)

echo "Welcome in screener linux for screen and server"
if [[ ! -f /bin/python3 ]] && [[ ! -f /usr/bin/python3 ]]; then
    echo "It needs to get python3, please install it :"
    sudo apt-get install -y python3
else
    echo "Python3 is installed... Ready to start screener !!"
fi

if [[ ! -f /bin/python3 ]] && [[ ! -f /usr/bin/python3 ]]; then
    echo "Sorry, but python3 isn't installed... It can't start screener"
else
    nohup python3 screener_screen.py &
    sleep 2 # Need a small time to let to screener to create usefull files
    nohup python3 server_screen.py &
fi
