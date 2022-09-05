import os
from time import strftime, sleep

import config_pyScreener as conf

# This is a log file with colours

class color:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    MALLOW = '\033[95m'
    WHITE = '\033[0m'
    BLACK = '\033[90m'

    NOT_BOLD = '\033[0m'
    NO_EFFECT = NOT_BOLD
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'

    ANIMATED = '\033[5m'
    ANIMATED2 = '\033[6m'

    BACKGROUNDED = '\033[7m'

    INVISIBLE = '\033[8m'

    ERRORED = '\033[9m'

def _print(string=""):
    for i in range(len(string)):
        os.write(conf.STDOUT, string[i].encode())

def cprint(contain="", statut=None, c0=color.CYAN, c1=color.YELLOW, c2=color.WHITE):
    time = strftime("%H:%M:%S")
    if statut == None:
        _print("{0}[ {1}{2} {0}] : {3}{4}{0}\n".format(color.NO_EFFECT, c0, time, c1, contain))
    else:
        _print("{0}[ {1}{2} {0}] [ {5}{6} {0}] : {3}{4}{0}\n".format(color.NO_EFFECT, c0, time, c1, contain, c2, statut))

def print_log(contain="No log !!"):
    cprint(contain, statut=" LOG ", c1=color.GREEN, c2=color.GREEN)

def print_error(contain="No error !!"):
    cprint(contain, statut="ERROR", c1=color.YELLOW, c2=color.RED)
    
def print_warn(contain="No warn !!"):
    cprint(contain, statut="WARN!", c1=color.WHITE, c2=color.YELLOW)
    
def print_info(contain="No info !!"):
    cprint(contain, statut="INFO!", c1=color.WHITE, c2=color.BLUE)

def print_test(contain="No info !!"):
    cprint(contain, statut="_TEST", c0=color.YELLOW, c1=color.CYAN, c2=color.MALLOW)

def print_debug(contain="No debug !!"):
    cprint(contain, statut="DEBUG", c0=color.RED, c1=color.GREEN, c2=color.CYAN)

def print_waiting(second):
    print_warn("Wait {0} seconds please !!".format(second))
    l = ("|", "\\", "-", "/", "|", "\\", "-", "/", "|", "|")
    i = 0; n = len(l)
    for _ in range(10 * second):
        print(l[i], end="", flush=True)
        sleep(0.1)
        print(chr(8), end="", flush=True)
        i += 1
        if i == n:
            i = 0

if __name__ == "__main__":
    _print("test\n")
    cprint("Test du printage !!", "LOG", c2=color.RED)
    print_info("test test")
    print_error("test test")
    print_log("test test")
    print_warn("test test")
    print_waiting(10)
