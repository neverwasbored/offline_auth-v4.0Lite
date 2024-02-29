import os
import json


class JsonData:
    def __init__(self, name: str):
        self.name = name
        try:
            path = os.path.join('.', 'data', f'{self.name}.json')
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            self.data = data
        except Exception as e:
            raise FileNotFoundError(f'Указанный файл не найден: {e}')
