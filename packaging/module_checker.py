from json import load
from os import listdir
from os.path import join, exists, isfile, split
from sys import stderr


class module_checker(object):
    def __init__(self):
        self.__checked = False
        self.__module_path = ''
        self.__parsed_modules = {}
        self.__info = []

    @property
    def info_list(self):
        return self.__info

    @property
    def module_list(self):
        if not self.__checked:
            self.check_module()
        return self.__parsed_modules

    @property
    def module_path(self):
        return self.__module_path

    @module_path.setter
    def module_path(self, value: str):
        self.__module_path = value

    def clean_status(self):
        self.__checked = False
        self.__parsed_modules = {}
        self.__info = []

    def check_module(self):
        self.clean_status()
        modules = {
            'resource': []
        }
        for module in listdir(self.module_path):
            status, info, data = self.__analyze_module(
                join(self.module_path, module))
            if status:
                modules[data.pop('type')].append(data)
            else:
                self.__info.append(f"Warning: {info}")
                print(f"\033[33mWarning: {info}\033[0m", file=stderr)
        self.__parsed_modules = modules
        self.__checked = True

    def __analyze_module(self, path: str):
        manifest = join(path, "module_manifest.json")
        dir_name = split(path)[1]
        if exists(manifest) and isfile(manifest):
            data = load(open(manifest, 'r', encoding='utf8'))
            for key in ('name', 'type', 'description'):
                if key not in data:
                    return False, f'In path "{dir_name}": Incomplete module_manifest.json, missing "{key}" field', None
            if dir_name != data['name']:
                return False, f'In path "{dir_name}": Does not match module name "{data["name"]}"', None
            if data['type'] != 'resource':
                return False, f'In path "{dir_name}": Unknown module type "{data["type"]}"', None
            return True, None, data
        else:
            return False, f'In path "{dir_name}": No module_manifest.json', None
