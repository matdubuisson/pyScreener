#!/bin/bash

last_command="stop"
fifo_file="about_screener/input_screener.fifo"

python3 kill_server_pyScreener.py
sleep 1
echo "" > $fifo_file
sleep 1
echo $last_command > $fifo_file
sleep 10
python3 kill_screener_pyScreener.py
