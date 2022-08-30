import os
import socket as sock
from time import sleep, strftime

import config_screen as conf

def launch_client():
    client_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    client_socket.connect(conf.datas["client"]["address"])

    conf.init_default("client", strftime("%H_%M_%S"))

    conf.registre_pid("client")

    pid = os.fork()
    if pid == 0: # reader
        conf.registre_pid("client")
        message = ""; failure = 0
        try:
            while True:
                message = client_socket.recv(1024).decode()
                print(message, flush=True, end="")
                if message == "":
                    failure = conf.mark_failure(failure, conf.datas["client"]["address"], "client_sending")
                    if failure == -1:
                        break
                else:
                    failure = 0
        except KeyboardInterrupt:
            conf.kill_pids("client", "registered_process_txt_file")
    
    else: # writer
        message = ""; failure = 0
        try:
            while True:
                message = input("")
                try:
                    client_socket.send(message.encode())
                    failure = 0
                except:
                    failure = conf.mark_failure(failure, conf.datas["client"]["address"], "client_sending")
                    if failure == -1:
                        break
        except KeyboardInterrupt: 
            conf.kill_pids("client", "registered_process_txt_file")

if __name__ == "__main__":
    launch_client()
