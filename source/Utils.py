from Log import Logger
from pathlib import Path

class PraseError(RuntimeError):
    pass

def get_yaml_files(path):
    path = Path(path)
    return [path / file for file in path.iterdir() if file.suffix == '.yml']

def check_dir(path):
    path = Path(path)
    if path.is_dir():
        return
    Logger.log(f'{path} 폴더가 없습니다 생성합니다', Logger.Level.WARNING)
    path.mkdir(exist_ok=True)


def check_files(path):
    if len(get_yaml_files(path)) <= 0:
        Logger.log(f'{path} 경로에 .yml 파일이 없습니다', Logger.Level.ERROR)
        return False    
    return True

def get_save_path(path):
    path = Path(path)
    save_path = Path(path).parent.parent / 'merged'
    save_path.mkdir(exist_ok=True)    
    return save_path / path.name


