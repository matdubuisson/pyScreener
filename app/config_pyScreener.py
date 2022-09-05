import os
import file_managing_pyScreener as fm
from printer_pyScreener import *

# Principal files descriptors :
STDIN = 0
STDOUT = 1
STDERR = 2

# Common between client and server :
#_ip = "185.142.53.128"
_ip = "127.0.0.1"
_port = 30000
_failure_limit = 5
_failure_delay = 0.5
_test_mode = False

datas = {
    # In the case here main_directory=?, it'll take the value
    # of os.getcwd(). In the point to avoid all problems, it's
    # better to put the address of the project but be sure about
    # the exact path !!
    "screener": {
        # Default datas :
        "directory": "-path about_screener",
        "input_fifo_file": "-fifo input_screener.fifo",
        "output_txt_file": "-reset_txt output_screener.txt",
        "registered_process_txt_file": "-reset_txt registered_process_screen.txt -in process/",
        #"presence_flag_file": "-reset_txt screener_presence.flag -in flag/",
        # Specific datas :
        "executable_bash_file": "-txt executable.bash",
        "max_length_for_output_txt_file": 10,
        "refresh_delay": 1,
        "test_file": "-txt test.txt -in zircoulouc"
    },
    "viewer": {
        #i Default datas :
        "directory": "-path about_viewer", # In fact, viewer uses screener to see the result
        "input_fifo_file": None,
        "output_txt_file": None,
        "registered_process_txt_file": "-reset_txt registered_process_viewer_{0}.txt", # {0} is the id 
        # in the case where there are several viewers
        #"presence_flag_file": "-reset_txt viewer_presence_{0}.flag",
        # Different things to view :
        "view_choices": ("screener", "server"),
        # Specific datasi :
        "refresh_delay": 0.1
    },
    "server": {
        # Default datas :
        "directory": "-path about_server",
        "input_fifo_file": "-fifo input_server.fifo",
        "output_txt_file": "-txt output_server.txt",
        "registered_process_txt_file": "-reset_txt registered_process_server.txt",
        #"presence_flag_file": "-reset_txt server_presence.flag",
        # Specific datas :
        "max_length_for_output_txt_file": 10,
        "refresh_delay": 1,
        # ==> Mod :
        "test_mode": _test_mode,
        # ==> Connecting :
        "ip": _ip,
        "port": _port,
        "address": (_ip, _port),
        "listening_length": 10,
        # ==> About clients :
        "client_registered_process_txt_file": "-txt registered_process_for_client_{0}.txt -in hold_clients/" # {0} is the ip and {1} is the port
    },
    "client": { # Means a client who is trying to connect to the server (not a process client of the server)
        # Default datas :
        "directory": "-path about_client",
        "input_fifo_file": None,
        "output_txt_file": None,
        "registered_process_txt_file": "-txt registered_process_client_{0}.txt -in process/", # Here {0} is an id
        #"presence_flag_file": "-txt client_presence_{0}.flag -in flags/",
        # Specific datas :
        # ==> Connecting :
        "ip": _ip,
        "port": _port,
        "address": (_ip, _port)
    }
}

def init_default(key="screener", information=None):
    path = datas[key].get("directory", None)
    if path == None:
        path = datas[key]["directory"] = os.curdir
    path = path.split(" ")[-1]
    fm.create_directory_file(path)
    os.chdir(path)
    for second_key in datas[key].keys():
        each = datas[key][second_key]
        if type(each) == str:
            each = each.split(" ")
            flag = False
            length = len(each)
            if length == 4:
                if each[2] == "-in":
                    flag = True
                    fm.create_directory_file(each[3])
                    os.chdir(each[3])
            #elif length != 2: # Here != 2 and 4
            #    raise SyntaxError("Data in config isn't valid : {0}".format(each))

            if information != None and length > 1:
                if "{0}" in each[1]:
                    save = each[1]
                    each[1] = save.format(information)
                    index = 0
                    while fm.is_in_path(each[1]):
                        each[1] = save.format(information + "_" + str(index))
                        index += 1
                    new_value = ""
                    for _each in each:
                        new_value += _each + " "
                    datas[key][second_key] = new_value
                    #print(key, second_key, new_value, datas[key][second_key])

            if each[0] == "-dir":
                fm.create_directory_file(each[1])
            elif each[0] == "-txt":
                fm.create_txt_file(each[1])
            elif each[0] == "-reset_txt":
                fm.remove_file(each[1])
                fm.create_txt_file(each[1])
            elif each[0] == "-fifo":
                fm.remove_file(each[1])
                fm.create_fifo_file(each[1])

            if flag:
                os.chdir(os.pardir)

    os.chdir(os.pardir)

def init_default_all():
    for each in datas.keys():
        init_default(each)

def reset(key="screener"):
    fm.remove_file(datas[key]["directory"].split(" ")[-1])
    init_default(key)

def reset_all():
    for each in datas.keys():
        reset(each)
    init_default_all()

def get_address(first_key, second_key, only_directory=False):
    line = datas[first_key][second_key]
    directory = datas[first_key]["directory"].split(" ")[-1]
    if directory[-1] != os.sep:
        directory += os.sep
    if second_key == "directory":
        return directory
    if type(line) != str:
        return None
    line = line.strip().split(" ")
    length = len(line)
    if length == 2:
        if only_directory:
            return directory
        return directory + line[1]
    elif length == 4:
        if only_directory:
            return directory + line[3]
        return directory + line[3] + line[1]
    else:
        return None

def registre_pid(first_key, second_key=None):
    if second_key == None:
        fm.add_line(get_address(first_key, "registered_process_txt_file"), os.getpid())
        return
    fm.add_line(get_address(first_key, second_key), os.getpid())

def kill_pids(first_key, second_key=None, only_directory=False, debug=False):
    addr = ""
    if second_key == None:
        addr = get_address(first_key, "registered_process_txt_file", only_directory)
    else:
        addr = get_address(first_key, second_key, only_directory)
    def kill_pids2(addr):
        result = ""; index=0
        while True:
            result = fm.read_line(addr, index)
            index += 1
            if result == None:
                break
            try:
                os.kill(int(result.strip()), 9)
                if debug:
                    print_debug("From {0}".format(addr))
                    print_debug("Kill process {0}".format(int(result.strip())))
                elif _test_mode:
                    print_test("From {0}".format(addr))
                    print_test("Kill process {0}".format(int(result.strip())))
            except ProcessLookupError:
                pass
            except ValueError:
                pass
        fm.remove_file(addr)
    if only_directory:
        os.chdir(addr)
        for each in os.listdir():
            if os.path.isfile(each):
                kill_pids2(each)
        os.chdir(os.pardir)
    else:
        kill_pids2(addr)

def mark_failure(failure, address, statut="no statut"):
    if failure == _failure_limit:
        print_info("Fatal attempt : Lost connection with {0}....".format(address))
        return -1
    print_error("Attempt {0} : {2} : No response of {1}....".format(failure, address, statut))
    sleep(_failure_delay)
    return failure + 1

if __name__ == "__main__":
    #init_default("screener")
    #print(get_address("screener", "executable_bash_file"))
    #print(get_address("-txt file.txt -in test/test/"))
    #registre_pid("screener")
    kill_pids("server", "client_registered_process_txt_file", True)
