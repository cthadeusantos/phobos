from source.system import System
from source.fileio import FileIO

import re

class Phobos():
    
    def __init__(self):
        file = FileIO()
        data = file.read(filename='data/entrada.json')
        print(data)
        file.save(data, 'data/saida.json')
        system = System(data=data)
        print(system)

    def get_setup(self, vpp=None, vpn=None, power_factor=None, root=None):
        return {'vpp': vpp, 'vpn': vpn, 'power_factor': power_factor, 'root': root}

    def only_integers(string):
        """Verifica se a string contém apenas números."""
        padrao = r"^\d+$"
        return re.match(padrao, string) is not None
    
    def is_number(string):
        """Verifica se a string é um número inteiro ou float."""
        padrao = r"^[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?$"
        return re.match(padrao, string) is not None
    


