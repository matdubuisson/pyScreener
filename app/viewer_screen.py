import os
from time import sleep, strftime

import config_screen as conf
import file_managing_screen as fm
from printer_screen import *

choices = conf.datas["viewer"]["view_choices"]
def launch_viewer():
    # Ask at the user to choose one program to access (for input and output)
    print_warn("Do you want to look screener or server ? Write screener or server to choose")
    choice = os.read(conf.STDIN, 100).decode().strip()
    while choice not in choices:
        print_error("Please choose of {0}".format(choices))
        choice = os.read(conf.STDIN, 100).decode().strip()

    # Init the directories and files system of viewer
    conf.init_default("viewer", strftime("%H_%M_%S"))

    # Create thread : first for to get the output and the seconde to set the input
    conf.registre_pid("viewer") # main pid
    pid = os.fork()

    if pid == 0:
        conf.registre_pid("viewer") # child pid
        fdo = os.open(conf.get_address(choice, "output_txt_file"), os.O_RDWR)
        try:
            while True:
                os.lseek(fdo, 0, os.SEEK_CUR)
                char = None
                while char != "":
                    try:
                        os.write(conf.STDOUT, os.read(fdo, 1))
                    except UnicodeDecodeError:
                        break
        except KeyboardInterrupt:
            pass
        os.close(fdo)

    else:
        fdi = os.open(conf.get_address(choice, "input_fifo_file"), os.O_RDWR)
        try:
            while True:
                os.write(fdi, os.read(conf.STDIN, 1))
        except KeyboardInterrupt:
            pass
        os.close(fdi)

if __name__ == "__main__":
    launch_viewer()
