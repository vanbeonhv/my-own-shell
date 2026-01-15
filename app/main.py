import os
import subprocess
import sys
class FileDetail:
    def __init__(self, name: str, path: str, is_executable: bool):
        self.name = name
        self.path = path
        self.is_executable = is_executable


# PATHS = ['D:\\apps\\Microsoft VS Code\\bin']
PATHS = os.environ['PATH'].split(os.pathsep)

def main():
    init_dir = os.getcwd()
    dir = [init_dir]


    while(True):
        sys.stdout.write("$ ")
        input_command = input()
        word_list = input_command.split()
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

# ================================================================
                
def echo_handler(word_list: list[str], context, dir) -> str:
    word_list.pop(0)
    print(' '.join(word_list))
    return 'CONTINUE'

def type_handler(word_list:list[str], command_map: dict, dir)-> str:
    # need handle case 'type' + blank comand
    main_command = word_list[1]
    is_found = False
    if main_command in command_map:
        print(f'{main_command} is a shell builtin')
        is_found = True
    else: 
        result = check_executable_files(main_command)
        # print('result', result)
        if(result.is_executable):
            print(f"{main_command} is {result.path}")
            is_found = True
    if(is_found is False): 
        print(f'{main_command}: not found')
    return 'CONTINUE'

def pwd_handler(word_list: list[str], context, dir: list[str]) -> str:
    print(dir[0])
    return 'CONTINUE'

def cd_handler(word_list: list[str], context, dir) -> str:
    if(len(word_list) > 2): 
        print("Too many args for cd command")
    path_agr = word_list[1]
    if(path_agr[0] == '/'):
        if(os.path.isdir(path_agr)):
            dir[0] = path_agr
        else:
            print(f"cd: {path_agr}: No such file or directory")

    return 'CONTINUE'


def check_executable_files(main_command: str):
    for path in PATHS:
        full_path = os.path.join(path, main_command)

        if sys.platform == "win32":
            return check_executable_file_window(full_path)
        else:
            is_executable = is_file_executable(full_path)
            if(is_executable):
                return FileDetail(main_command, full_path, is_executable)
    return FileDetail('', '', False)

def check_executable_file_window(full_path):
    window_extensions = ['.exe', '.cmd']
    for extension in window_extensions:
        absolute_path = full_path + extension
        is_executable = is_file_executable(absolute_path)
        if(is_executable):
            # ở window, để execute file thì phải truyền full path + extentions. Linux thì chỉ cần name
            return FileDetail(absolute_path, absolute_path, is_executable)

def is_file_executable(full_path: str):
    if(os.path.isfile(full_path)):
        return os.access(full_path, os.X_OK)
    return False


if __name__ == "__main__":
    main()
