from pathlib import Path
from colorama import init, Back, Style
from enum import Enum

class Logger:

    class Level(Enum):
        LOG = Style.NORMAL
        WARNING = Back.YELLOW
        ERROR = Back.RED
        INFO = Back.GREEN

    class PrintMod(Enum):
        DEBUG = 0
        NORMAL = 1
        FILE = 2

    is_initialized = False
    print_mod = PrintMod.NORMAL
    log_file_path = None

    @staticmethod
    def __initialize():
        init(autoreset=True)
        Logger.is_initialized = True
        if Logger.log_file_path and Logger.log_file_path.exists():
            Logger.log_file_path.unlink()
        Logger.log(f'Logger is initialized')
    
    @staticmethod
    def log(msg, level=Level.LOG):
        if not Logger.is_initialized:
            Logger.__initialize()
        if Logger.print_mod == Logger.PrintMod.NORMAL and level == Logger.Level.LOG:
            return
        
        if Logger.print_mod.value <= Logger.PrintMod.NORMAL.value:
            print(f'{level.value}{msg}')
        else:
            print(msg, file=open(Logger.log_file_path, 'a', encoding='utf-8'))
    
    @staticmethod
    def set_print_mode(mod):
        Logger.print_mod = mod
    
    @staticmethod
    def set_working_path(working_path):
        log_folder = working_path / 'log'
        log_folder.mkdir(exist_ok=True)
        Logger.log_file_path = log_folder / 'log.txt'
