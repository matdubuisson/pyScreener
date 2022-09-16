# Author : matdubuisson
# Source : https://github.com/matdubuisson/pyScreener
# Licence : Apache (2)

import os

# -1 : Work not done or done with error
# 0 : No work to make
# 1 : Work done

def is_in_path(fileName):
    """
    pre: fileName is a file or a directory
    post: Return True if it is in the current path else False
    """
    for each in os.listdir():
        if fileName == each:
            return True
    return False

def create_txt_file(fileName):
    """
    pre: fileName is a file name
    post: Create a text file, return 0 if the file is already existing
    and return -1 if the name isn't valid
    """
    if fileName == None:
        return -1
    elif is_in_path(fileName):
        return 0
    os.close(os.open(fileName, os.O_CREAT))
    return 1

def create_fifo_file(fileName):
    """
    pre: fileName is a file name
    post: Create a fifo, return 0 if the file is already existing
    and return -1 if the name isn't valid
    """
    if fileName == None:
        return -1
    elif is_in_path(fileName):
        return 0
    os.mkfifo(fileName)
    return 1

def create_directory_file(fileName):
    """
    pre: fileName is a directory name
    post: Create a directory, return 0 if the file is already existing
    and return -1 if the name isn't valid
    """
    if fileName == None:
        return -1
    elif is_in_path(fileName):
        return 0
    path = fileName.replace(os.sep, "/").split("/")
    current_path = os.getcwd()
    for i in range(len(path)):
        if path[i] == "":
            pass
        elif not is_in_path(path[i]):
            os.mkdir(path[i])
            os.chdir(path[i])
        else:
            os.chdir(path[i])
    os.chdir(current_path)
    return 1

def remove_file(fileName):
    """
    pre: fileName is the name of a file or a directory
    post: Remove recusively the file or directory
    Return 0 if the file doesn't exist else return 1
    """
    if fileName == None or not is_in_path(fileName):
        return 0
    def remove_file2(fileName):
        if not os.path.isdir(fileName):
            os.remove(fileName)
            return
        os.chdir(fileName)
        for each in os.listdir():
            remove_file(each)
        os.chdir(os.pardir)
        os.rmdir(fileName)
    remove_file2(fileName)
    return 1

def get_file_length(fileName, targeted_char=None):
    """
    pre: filename is the name of a txt file
    targeted_char is a specified character
    post: Return the number of character in the file
    or return the number of 'targeted_char' present
    in this file
    """
    count = 0
    fd = os.open(fileName, os.O_RDONLY)
    os.lseek(fd, 0, os.SEEK_SET)
    char = None
    while char != "":
        char = os.read(fd, 1).decode()
        if targeted_char == None or char == targeted_char:
            count += 1
    os.close(fd)
    return count

def get_file_length2(fileName, targeted_char):
    """
    pre: filename is the name of a txt file
    targeted_char is a specified character
    post: Return  atuple with as first element 
    the number of character in the file and as
    second element the number of 'targeted_char'
    present in this file
    """
    count = 0; total_count = 0
    fd = os.open(fileName, os.O_RDONLY)
    os.lseek(fd, 0, os.SEEK_SET)
    char = None
    while char != "":
        char = os.read(fd, 1).decode()
        if targeted_char == None or char == targeted_char:
            count += 1
        total_count += 1
    os.close(fd)
    return (count, total_count)

def clear_file(fileName):
    """
    pre: filename is the name of a txt file
    post: Empty the contain of the file without deleting it
    """
    fd = os.open(fileName, os.O_WRONLY)
    for _ in range(get_file_length(fileName)):
        os.write(fd, chr(8).encode())
    os.close(fd)

def add_line(fileName, line):
    """
    pre: filename is the name of a txt file and
    line is a string
    post: Write the line 'line' in the end of the file 'filename'
    """
    line = str(line)
    fd = os.open(fileName, os.O_WRONLY)
    os.lseek(fd, 0, os.SEEK_END)
    for char in line:
        os.write(fd, char.encode())
    os.write(fd, "\n".encode())
    os.close(fd)

def read_line(fileName, line_index=0):
    """
    pre: filename is the name of a txt file and
    line_index is an integer >= 0
    post: Return the line in the file 'filename'
    at the index 'line_index'. If the line doesn't
    exist it returns None
    """
    fd = os.open(fileName, os.O_RDWR)
    os.lseek(fd, 0, os.SEEK_SET)
    index = 0; line = ""
    while True:
        char = os.read(fd, 1).decode()
        if char == "":
            break
        elif char == "\n":
            index += 1
        if index == line_index:
            line += char
    os.close(fd)
    if line == "":
        return None
    return line

if __name__ == "__main__":
    #print(is_in_path("test.txt"), is_in_path("qfsfhdfqidsoi.djsdi"))
    #create_directory_file("test/test/retest"); os.chdir("test")
    #create_txt_file("test.txt"); create_fifo_file("retset.fifo")
    #os.chdir(os.pardir)
    #create_txt_file("test.txt")
    #remove_file("test.txt")
    #remove_file("test")
    create_txt_file("test.txt")
    print(is_in_path("test.txt"))
    print(os.listdir())
    #add_line("test.txt", "Salut comment ca va ?\nYolo !!")
    #print(read_line("test.txt", 14))
    #clear_file("test.txt")
