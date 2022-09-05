import os
from time import sleep

import config_pyScreener as conf
import file_managing_pyScreener as fm

def launch_screener():
    conf.init_default("screener") # Create files system of screener
    conf.registre_pid("screener") # main pid

    fdo = os.open(conf.get_address("screener", "output_txt_file"), os.O_RDWR) # For all output
    fdi = os.open(conf.get_address("screener", "input_fifo_file"), os.O_RDWR) # For all input

    os.dup2(fdo, conf.STDOUT) # Redirect stdout => fdo
    os.dup2(fdi, conf.STDIN) # Redirect stdin => fdi

    pid = os.fork()
    if pid == 0: # child
        conf.registre_pid("screener") # child pid
        # Execute the specified bash executable
        os.system("bash {0}".format(conf.get_address("screener", "executable_bash_file")))
        exit(0) # For child
    else: # main
        pid2 = os.fork()
        sleep(0.01)
        if pid2 == 0: # main-child
            conf.registre_pid("screener") # main-child pid
            # This part limits the length of the output file of screener in the point to
            # limit the work of the server
            fileName = conf.get_address("screener", "output_txt_file")
            while True:
                if fm.get_file_length(fileName, "\n") > conf.datas["screener"]["max_length_for_output_txt_file"]:
                    sleep(0.1)
                    fm.clear_file(fileName)
                sleep(conf.datas["screener"]["refresh_delay"])
        else: # main-main
            os.wait()

    os.close(fdo)
    os.close(fdi)

if __name__ == "__main__":
    launch_screener()
