from pathlib import Path
import argparse
from colorama.initialise import init
from Utils import *
from Yaml import *
from Log import Logger

def merge(en_path, ko_path):
    Logger.log(f'en을 ko와 합칩니다\n\t{en_path}\n\t{ko_path}', Logger.Level.INFO)
    en_resources = YamlFiles(en_path)
    ko_resources = YamlFiles(ko_path)

    for resource in en_resources:
        for key in resource:
            Logger.log(f'{key}')
            ko_entity = ko_resources[key]
            if ko_entity:
                en_entity = resource[key]
                if ko_entity.is_comment():
                    Logger.log(f'\t{ko_entity}를 찾았지만, 주석입니다')
                    continue
                if en_entity.string == ko_entity.string:
                    Logger.log(f'\ten과 ko가 동일합니다')
                    continue
                Logger.log(f'\t원본 : {en_entity.string}\n\t대체 : {ko_entity.string}')
                en_entity.string = ko_entity.string
            else:
                Logger.log(f'\t{key}가 en에는 있지만, ko에는 없습니다.')
    
    en_resources.save()


def main(working_path):
    en_path = working_path / 'en'
    ko_path = working_path / 'ko'

    if not (check_dir(en_path) and check_dir(ko_path)):
        return

    if not (check_files(en_path) and check_files(ko_path)):
        return

    merge(en_path, ko_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--print', type=str, help='출력 모드를 설정합니다, DEBUG, CONSOLE, FILE')

    args = parser.parse_args()


    working_path = Path.cwd()

    Logger.set_working_path(working_path)

    if args.print == 'DEBUG':
        Logger.set_print_mode(Logger.PrintMod.DEBUG)
    elif args.print == 'NORMAL':
        Logger.set_print_mode(Logger.PrintMod.NORMAL)
    elif args.print == 'FILE':
        Logger.set_print_mode(Logger.PrintMod.FILE)
    else:
        Logger.set_print_mode(Logger.PrintMod.NORMAL)

    Logger.log(f'Working Path : {working_path}')
    main(working_path)

