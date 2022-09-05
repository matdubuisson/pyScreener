import os
import socket as sock
from time import sleep, strftime

import config_pyScreener as conf

def launch_client():
    client_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    client_socket.connect(conf.datas["client"]["address"])

    conf.init_default("client", strftime("%H_%M_%S"))

    conf.registre_pid("client")

    pid = os.fork()
    if pid == 0: # reader, child
        conf.registre_pid("client")
        message = ""; failure = 0
        try:
            while True:
                message = client_socket.recv(1024).decode()
                os.write(conf.STDOUT, message.encode())
                if message == "":
                    # Re-attempt to connect, if no possibilities, it disconnect with the server
                    failure = conf.mark_failure(failure, conf.datas["client"]["address"], "client_sending")
                    if failure == -1:
                        break
                else:
                    failure = 0
        except KeyboardInterrupt:
            conf.kill_pids("client", "registered_process_txt_file")
    
    else: # writer, main
        message = ""; failure = 0
        try:
            while True:
                message = os.read(conf.STDIN, 100).decode().strip()
                try:
                    client_socket.send(message.encode())
                    failure = 0
                except:
                    # Re-attempt to connect, if no possibilities, it disconnect with the user
                    failure = conf.mark_failure(failure, conf.datas["client"]["address"], "client_sending")
                    if failure == -1:
                        break
        except KeyboardInterrupt: 
            conf.kill_pids("client", "registered_process_txt_file")

if __name__ == "__main__":
    launch_client()
