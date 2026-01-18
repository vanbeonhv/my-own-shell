# =====================Handler=================================
                
import os

from app.utils import check_executable_files, get_home_directory
SEP = os.sep


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