import os
import json

class FileIO:

    def __init__(self, filename=None):
        self.filename=filename

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value=None):
        if value is not None:
            if not isinstance(value, str):
                raise TypeError("Invalid filename typeerror!")
        self._filename = value

    def read(self, filename=None):
        if self.filename is None and filename is None:
            raise AttributeError('Empty filename!')
        if self.filename is None and filename is not None:
            self.filename = filename

        try:
            with open(self.filename, 'r') as arquivo:
                data = json.load(arquivo)
                return data
        except FileNotFoundError:
            print('Arquivo não encontrado.')
        except json.JSONDecodeError:
            print('Conteúdo do arquivo não é um JSON válido.')
        return data
        
    def save(self, data=None, output=None):
        if data is None:
            raise AttributeError('Empty data!')
        if output is None:
            raise AttributeError('Empty filename!')
        try:
            with open(output, 'w') as jsonfile:
                json.dump(data, jsonfile, indent=4, sort_keys=True)
        except FileNotFoundError:
            print('Arquivo não encontrado.')
            with open(output, 'w') as arquivo:
                json.dump('', arquivo, indent=4)
        except json.JSONDecodeError:
            print('Conteúdo do arquivo não é um JSON válido.')

    def check_if_path_exists(self, path):
        return os.path.exists(path)
    
