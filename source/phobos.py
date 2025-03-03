from source.system import System

import re

class Phobos(System):
    
    # def __init__(self):
    #     # file = FileIO()
    #     # data = file.read(filename='data/entrada.json')
    #     # print(data)
    #     # file.save(data, 'data/saida.json')
    #     # system = System(data=data)
    #     # print(system)
    #     system = System()

    def __init__(self, root=None, vline=0, vphase=0, power_factor=0, data=None):
        super().__init__(root, vline, vphase, power_factor, data)

    @staticmethod
    def only_integers(string):
        """Verifica se a string contém apenas números."""
        padrao = r"^\d+$"
        return re.match(padrao, string) is not None
    
    @staticmethod
    def is_number(string):
        """Verifica se a string é um número inteiro ou float."""
        padrao = r"^[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?$"
        return re.match(padrao, string) is not None
    


