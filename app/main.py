import os
import sys
from unittest import result

# PATH="/usr/bin:/usr/local/bin:"

def main():
    while(True):
        sys.stdout.write("$ ")
        command = input()
        word_list = command.split()
        first_word = word_list[0]
        word_list.pop(0)

        command_map = {
            'echo': echo_handler,
            'type': type_handler,
            'exit': lambda x, y: 'EXIT'
        }

        if first_word in command_map:
            result = command_map[first_word](word_list, command_map)
            if(result == 'EXIT'): 
                break
        else:
            print(f"{command}: command not found")
                
def echo_handler(word_list: list[str], context):
    print(' '.join(word_list))

def type_handler(word_list:list[str], command_map: dict):
    arguments = ' '.join(word_list)
    is_found = False
    if arguments in command_map:
        print(f'{arguments} is a shell builtin')
        is_found = True
    else: 
        paths = os.environ['PATH'].split(os.pathsep)
        for path in paths:
            full_path = os.path.join(path, arguments)
            result = check_executable_files(full_path)
            if(result):
                print(f"{arguments} is {full_path}")
                is_found = True
                break

    if(is_found is False): 
        print(f'{arguments}: not found')

def check_executable_files(full_path: str):
    if(os.path.isfile(full_path)):
        return os.access(full_path, os.X_OK)
    return False


if __name__ == "__main__":
    main()
