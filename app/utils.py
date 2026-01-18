import os
import sys

# PATHS = ['D:\\apps\\Microsoft VS Code\\bin']
PATHS = os.environ['PATH'].split(os.pathsep)

class FileDetail:
    def __init__(self, name: str, path: str, is_executable: bool):
        self.name = name
        self.path = path
        self.is_executable = is_executable

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