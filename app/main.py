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
SEP = os.sep

def main():
    init_dir = os.getcwd()
    dir = {'current': init_dir}

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

# =====================Handler=================================
                
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

def pwd_handler(word_list: list[str], context, dir: dict) -> str:
    print(dir['current'])
    return 'CONTINUE'

def cd_handler(word_list: list[str], context, dir: dict) -> str:
    if(len(word_list) > 2): 
        print("Too many args for cd command")
    path_input = word_list[1]
    if(path_input[0] == '/'):
        if(os.path.isdir(path_input)):
            dir['current'] = path_input
        else:
            print(f"cd: {path_input}: No such file or directory")
    else:
        cd_relative(path_input, dir)

    return 'CONTINUE'

def cd_relative(path_input: str, dir: dict):
    if('/' in path_input):
        folders = path_input.split('/')
        if(folders[0] == '.'):
            next_dir_str = SEP.join(folders[1:])
            handle_sub_directory(next_dir_str, dir)
            return
        if(folders[0] == '..'):
            no_of_back = 0
            for text in folders:
                if text == '..':
                    no_of_back = no_of_back + 1
                else: 
                    break
            cur_dir_list = dir['current'].split(SEP)
            base_dir = cur_dir_list[:-1 * no_of_back]
            dir['current'] = SEP.join(base_dir)
            
            next_dir = folders[no_of_back:]
            next_dir_str = SEP.join(next_dir)
            handle_sub_directory(next_dir_str, dir)
            return
        if(folders[0] == '~'):
            dir['current'] = get_home_directory()
            next_dir_str = SEP.join(folders[1:])
            handle_sub_directory(next_dir_str, dir)
            return
    if(path_input == '~'):
        dir['current'] = get_home_directory()
        handle_sub_directory('', dir)
    else:
        handle_sub_directory(path_input, dir)

def handle_sub_directory(path_input: str, dir: dict):
    """Case user nhập thẳng folder kế tiếp
    """
    # Không có folder, thì nghĩa thuần go back.
    if(path_input == ''):
        target_dir = dir['current']
    else:
        target_dir = os.path.join(dir['current'], path_input)
    if(os.path.isdir(target_dir)):
        dir['current'] = target_dir
    else:
        print(f"cd: {path_input}: No such file or directory")


# ====================== Util============================
def check_executable_files(main_command: str):
    if sys.platform == "win32":
        return check_executable_file_window(main_command)
    else:
        for path in PATHS:
            full_path = os.path.join(path, main_command)
            is_executable = is_file_executable(full_path)
            if(is_executable):
                return FileDetail(main_command, full_path, is_executable)
        return FileDetail('', '', False)

def check_executable_file_window(main_command):
    for path in PATHS:
        full_path = os.path.join(path, main_command)
        window_extensions = ['.exe', '.cmd', '.bat']
        for extension in window_extensions:
            absolute_path = full_path + extension
            is_executable = is_file_executable(absolute_path)
            if(is_executable):
                # ở window, để execute file thì phải truyền full path + extentions. Linux thì chỉ cần name
                return FileDetail(absolute_path, absolute_path, is_executable)
    return FileDetail('', '', False)

def is_file_executable(full_path: str):
    if(os.path.isfile(full_path)):
        return os.access(full_path, os.X_OK)
    return False

def get_home_directory() -> str:
    """Thằng window nó lại phải ghép từ 2 biến, Linux thì cứ lấy thẳng"""
    if sys.platform == "win32":
        home_drive = os.getenv('HOMEDRIVE', '')
        home_path = os.getenv('HOMEPATH', '')
        if home_drive and home_path:
            return home_drive + home_path
        # Fallback to USERPROFILE
        return os.getenv('USERPROFILE', '')
    else:
        return os.getenv('HOME', '')


if __name__ == "__main__":
    main()
