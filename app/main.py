import os
import shlex
import subprocess
import sys
from app.cmd_handler import cd_handler, pwd_handler, type_handler, echo_handler
from app.utils import check_executable_files

def main():
    init_dir = os.getcwd()
    dir = {'current': init_dir}

    while(True):
        sys.stdout.write("$ ")
        input_command = input()
        word_list = shlex.split(input_command)
        first_word = word_list[0]

        command_map = {
            'echo': echo_handler,
            'type': type_handler,
            'pwd': pwd_handler,
            'cd': cd_handler,
            'exit': lambda x, y, z: 'EXIT'
        }

        if first_word in command_map:
            result = command_map[first_word](word_list, command_map, dir)
            if(result == 'EXIT'): 
                break
            if(result == 'CONTINUE'):
                continue
            
        execute_check_result = check_executable_files(word_list[0])
        if(execute_check_result.is_executable):
            # sub process nhận là dạng list string ['fullpath_extention', 'argument']
            subprocess.run([execute_check_result.name] + word_list[1:])
        else:
            print(f"{input_command}: command not found")

if __name__ == "__main__":
    main()
