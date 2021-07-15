import re
from pathlib import Path
from Log import Logger
from Utils import PraseError, get_yaml_files, get_save_path

YAML_REGEX = re.compile('([a-zA-Z0-9_\.]+)\s*:\s*([0-9])*\s*\"(.*)\"|(#.*#*)')
KOREAN_REGEX = re.compile('[가-힣]+')

class YamlEntity:
    def __init__(self, key, string, order, tag):
        self.key = key
        self.string = string
        self.order = order
        self.tag = tag

    def is_comment(self):
        return self.tag == '#'
    
    def has_korean(self):
        return KOREAN_REGEX.search(self.string)
    
    def __repr__(self):
        if self.tag == '#':
            return f'{self.key}'
        else:
            return f'{self.key}:{self.tag} \"{self.string}\"'

class YamlResource:
    def __init__(self, path, datas):
        self.path = path
        self.entities = {}

        for order, data in enumerate(datas):
            key, string, tag = '', '', ''
            if data[0] != '':
                key = data[0]
                tag = data[1]
                string = data[2]
            elif data[3] != '':
                key = data[3]
                tag = '#'
                string = data[3]

            self.entities[key] = YamlEntity(key, string, order, tag)
    
    def __getitem__(self, key):
        return self.entities[key]
    
    def __contains__(self, key):
        return key in self.entities
    
    def __iter__(self):
        return iter(self.entities.keys())

    def __repr__(self):
        newline = '\n'
        return f'{newline.join(repr(entity) for entity in self.entities.values())}'

class YamlFiles:
    def __init__(self, path):
        self.resources = {}
        
        paths = get_yaml_files(path)
        self.resources = parse_all_files(paths)
    
    def save(self):
        for path in self.resources:
            Logger.log(f'{Path(path).name}를 저장하는 중')
            try:
                with get_save_path(path).open(mode='w', encoding='utf-8') as f:
                    f.write(u'\uFEFF')
                    f.write('l_english:\n\n')
                    f.write(repr(self.resources[path]))
                    Logger.log(f'{Path(path).name}을 성공적으로 저장했습니다', Logger.Level.INFO)
            except:
                Logger.log(f'{Path(path).name}을 저장할 수 없습니다', Logger.Level.ERROR)


    def __getitem__(self, key):
        for resource in self:
            if key in resource:
                return resource[key]
        return None
    
    def __iter__(self):
        return iter(self.resources.values())

def parse(path):
    try:
        Logger.log(f'{Path(path).name}을 불러오는 중')
        with open(path, 'r', encoding='utf-8') as f:
            datas = YAML_REGEX.findall(f.read())
            Logger.log(f'{Path(path).name}을 성공적으로 불러왔습니다', Logger.Level.INFO)
            return YamlResource(path, datas)
    except OSError as err:
        Logger.log(f'{Path(path).name}을 불러올 수 없습니다', Logger.Level.ERROR)
        raise PraseError(err)


def parse_all_files(paths):
    return {path:parse(path) for path in paths}

        