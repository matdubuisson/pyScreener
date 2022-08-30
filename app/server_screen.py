import os
import socket as sock
from time import sleep

import config_screen as conf
import file_managing_screen as fm
from printer_screen import *

server_socket = main_pid = fdo = fdi = None

##########################################################

def reader(conn, addr, client_processes_file):
    fileName = fd = None
    if not conf.datas["server"]["test_mode"]:
        fileName = conf.get_address("screener", "input_fifo_file")
        fd = os.open(fileName, os.O_WRONLY)
    failure = 0
    while True:
        # Receive the string to set
        message = conn.recv(1024).decode()
        if message == "":
            # Re-attempt to connect, if no possibilities, it disconnect with the user
            failure = conf.mark_failure(failure, addr, "receiving")
            if failure == -1:
                break
        # Set the string
        else:
            failure = 0
            if conf.datas["server"]["test_mode"]:
                print_test("Read message from {0} ==> {1} !!".format(addr, message))

            else:
                os.write(fd, "{0}\n".format(message).encode())
                sleep(0.01)
    if not conf.datas["server"]["test_mode"]:
        os.close(fd)
    conf.kill_pids("server", "client_registered_process_txt_file")

######################################################

def writer(conn, addr, client_processes_file):
    fileName = fd = None
    if not conf.datas["server"]["test_mode"]:
        fileName = conf.get_address("screener", "output_txt_file")
        fd = os.open(fileName, os.O_RDONLY)
    failure = 0
    while True:
        message = ""
        # Get the string to send
        if conf.datas["server"]["test_mode"]:
            print_test("Write test message :")
            message = input("")
            if message == "":
                message = "Yolo !!"
        else:
            char = None
            while char != "":
                try:
                    char = os.read(fd, 1).decode()
                    message += char
                except UnicodeDecodeError:
                    break
        # Send the string
        is_sent = False
        while not is_sent:
            try:
                conn.send(message.encode())
                failure = 0; is_sent = True
            except:
                # Re-attempt to connect, if no possibilities, it disconnect with the user
                failure = conf.mark_failure(failure, addr, "sending")
                if failure == -1:
                    break
        if failure == -1:
            break
    if not conf.datas["server"]["test_mode"]:
        os.close(fd)
    conf.kill_pids("server", "client_registered_process_txt_file")

##########################################################

def session(conn, addr):
    conf.init_default("server", "hold_client") # Create file system for this client
    client_processes_file = conf.get_address("server", "client_registered_process_txt_file") # The file of this address is generated with the previous line (init)
    try:
        print_info("New client {0} !!".format(addr))
        conf.registre_pid("server", "client_registered_process_txt_file") # For main, avoid confusion
        pid = os.fork()
        if pid == 0: # reader
            conf.registre_pid("server", "client_registered_process_txt_file") # For child
            reader(conn, addr, client_processes_file)
        else: # writer
            writer(conn, addr, client_processes_file)
    except BrokenPipeError: # If the server breaks the processus
        pass
    except ConnectionResetError: # If the client does a brutal disconnection
        print_info("Connection has been reset by client {0} !!".format(addr))

##########################################################

clients_list = [] # Registre each client in the shape of a tuple
# with (connection, address)
def accepter(server_socket):
    global main_pid
    global clients_list

    # This part listens the coming of the new clients
    # It accepts them and launches them
    print_info("The server is started !!")
    while True:
        client_connection, client_addr = server_socket.accept()
        clients_list.append((client_connection, client_addr))
        print_warn("Acceptation of {0} !!".format(client_addr))
        
        pid = os.fork()
        if pid == 0:
            # Always pass connection and address
            session(client_connection, client_addr)
            return

##########################################################

def shutdown():
    global main_pid
    global clients_list
    global server_socket
    global fdo
    global fdi
    
    if main_pid == 0:
        return # Nothing to do
    # Before, closing all clients connections
    for conn, addr in clients_list:
        print_info("Closing of {0}....".format(addr))
        conn.close()
        print_info("Done !!")
    print_info("Closing of the server....")
    server_socket.close() # Close server socket
    print_info("Done !!")
    # Close input and output txt file
    if fdo != None:
        os.close(fdo)
    if fdi != None:
        os.close(fdi)
    # Kill all clients processus
    conf.kill_pids("server", "client_registered_process_txt_file", True)
    # Shutdown could kill itself without a finished work so it creates an
    # 'anonymous' process to avoid it
    pid = os.fork()
    if pid == 0:
        # Kill server processus
        conf.kill_pids("server")

##########################################################

def launch_server():
    conf.init_default("server") # Create file system of server

    fdo = os.open(conf.get_address("server", "output_txt_file"), os.O_RDWR)
    fdi = os.open(conf.get_address("server", "input_fifo_file"), os.O_RDWR)
    
    os.dup2(fdo, conf.STDOUT) # Redirect stdout => fdo
    os.dup2(fdi, conf.STDIN) # Redirect stdin => fdi
    print_info("STARTING OF THE SERVER IN BACKGROUND !!")
    
    global server_socket
    global main_pid

    server_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    server_socket.bind(conf.datas["server"]["address"])
    server_socket.listen(conf.datas["server"]["listening_length"])

    main_pid = os.getpid()
    conf.registre_pid("server") # principal main pid
    pid = os.fork()
    if pid == 0:
        # This processus has never finished and it needs to be killed
        conf.registre_pid("server") # child pid
        sleep(0.01)
        # Limit the length of the output txt file fdo
        fileName = conf.get_address("server", "output_txt_file")
        while True:
            if fm.get_file_length(fileName, "\n") > conf.datas["server"]["max_length_for_output_txt_file"]:
                sleep(0.1)
                fm.clear_file(fileName)
            sleep(conf.datas["server"]["refresh_delay"])

    try:
        accepter(server_socket) # Start server
        shutdown()
    except KeyboardInterrupt:
        shutdown()

if __name__ == "__main__":
    launch_server()
