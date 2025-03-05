import unittest

from source.system import System
from source.vertex import Vertex
from source.database import CableDBMT
from source.cable import Cable
from source.fileio import FileIO

class TestSystem(unittest.TestCase):

    def setUp(self):
        #return super().setUp()
        self.system = System()
        #self.system2 = System()
        self.file = FileIO()
        self.cable_db = CableDBMT('databases/mt.db')

    def test_insert_parameters(self):
        data = { 'root': '1', 'vpp': 220, 'vpn': 127, 'power_factor': 0.5 }
        phobos = System(data=data)
        self.assertEqual(phobos.get_setup(), {'root': '1', 'vpp': 220, 'vpn': 127, 'power_factor': 0.5})

        phobos = System(root='10', vpp=125, vpn=96, power_factor=0.8)
        self.assertEqual(phobos.get_setup(), {'root': '10', 'vpp': 125, 'vpn': 96, 'power_factor': 0.8})

    def test_root(self):
        self.system.root = 10
        self.assertIsInstance(self.system.root, int)
        self.assertEqual(self.system.root, 10)
        
        with self.assertRaises(ValueError):
            self.system.root = -5  # Tentativa de atribuir um valor negativo

        with self.assertRaises(TypeError):
            self.system.root = Vertex()  # Tentativa de atribuir um valor negativo

    def test_power_factor(self):
        self.system.power_factor = 1
        self.assertIsInstance(self.system.power_factor, int)
        self.assertEqual(self.system.power_factor, 1)
        self.system.power_factor = .5
        self.assertIsInstance(self.system.power_factor, float)
        self.assertEqual(self.system.power_factor, .5)
        
        with self.assertRaises(ValueError):
            self.system.power_factor = 2.3  # Tentativa de atribuir um valor negativo

        with self.assertRaises(TypeError):
            self.system.power_factor = (1,4)  # Tentativa de atribuir um valor negativo

    def test_vpp(self):
        self.system.vpp = 220
        self.assertIsInstance(self.system.vpp, int)
        self.assertEqual(self.system.vpp, 220)
        self.system.vpp = 127.5
        self.assertIsInstance(self.system.vpp, float)
        self.assertEqual(self.system.vpp, 127.5)
        
        with self.assertRaises(ValueError):
            self.system.vpp = -6.3  # Tentativa de atribuir um valor negativo
        with self.assertRaises(TypeError):
            self.system.vpn = (1,4)  # Tentativa de atribuir um tipo invalido
            
    def test_vpn(self):
        self.system.vpn = 220
        self.assertIsInstance(self.system.vpn, int)
        self.assertEqual(self.system.vpn, 220)
        self.system.vpn = 127.5
        self.assertIsInstance(self.system.vpn, float)
        self.assertEqual(self.system.vpn, 127.5)
        
        with self.assertRaises(ValueError):
            self.system.vpn = -6.3  # Tentativa de atribuir um valor negativo
        with self.assertRaises(TypeError):
            self.system.vpn = (1,4)  # Tentativa de atribuir um tipo invalido

        self.system.add_edge('A','B', 0, 10)
        self.system.add_edge('A','C', 0, 20)
        self.system.add_edge('C','D', 0, 30)
        self.system.add_edge('D','F', 0, 40)
        self.system.add_edge('E','B', 0, 50)
        self.system.add_edge('E','G', 0, 60)

    # def test_system_creation(self):
    #     self.assertEqual(self.system2.vertices, {})

    # def test_root_setter(self):
    #     self.system2.root = 10
    #     self.assertIsInstance(self.system2.root, int)
    #     self.assertEqual(self.system2.root, 10)

    #     self.system2.root = "A"
    #     self.assertIsInstance(self.system2.root, str)
    #     self.assertEqual(self.system2.root, 'A')
        
    #     with self.assertRaises(TypeError):
    #         self.system2.root = Vertex()  # Tentativa de atribuir uma string não numérica
    #     with self.assertRaises(ValueError):
    #         self.system2.root = -5  # Tentativa de atribuir um valor negativo
    
    def test_DFS_expert(self):
        self.system.reset()
        self.system.add_edge('A','B', 10, 10)
        self.system.add_edge('A','C', 20, 20)
        self.system.add_edge('C','D', 30, 30)
        self.system.add_edge('D','F', 40, 40)
        self.system.add_edge('E','B', 50, 50)
        self.system.add_edge('E','G', 60, 60)
        self.system.add_edge('D','H', 110, 60)

        self.system.update_vertex('A', weight=4)
        self.system.update_vertex('B', weight=8)
        self.system.update_vertex('C', weight=16)
        self.system.update_vertex('D', weight=32)
        self.system.update_vertex('E', weight=64)
        self.system.update_vertex('F', weight=128)
        self.system.update_vertex('G', weight=256)
        self.system.update_vertex('H', weight=512)

        self.system.root='A'
        #cargas = self.system.DFS_expert('A')
        cargas = self.system.accumulate_payload()
        self.assertEqual(self.system.payload_list(), {'A': 1340, 'B': 438, 'C': 868, 'D': 822, 'F': 128, 'E': 380, 'G': 256, 'H': 512})

    def test_kfactor(self):
        self.system.reset()

        cable1 = Cable()
        cable1.setting(self.cable_db.get_cable_especifications(id=180, installation=1))
        cable2 = Cable()
        cable2.setting(self.cable_db.get_cable_especifications(id=150, installation=0))
        cable3 = Cable()
        cable3.setting(self.cable_db.get_cable_especifications(id=88, installation=0))

        self.system.vpp=13.8
        self.system.vpn=13.8
        self.system.power_factor=0.9
        self.system.root='A'

        self.system.set_vn(self.system.vpp)

        self.system.add_edge('A','B', 10, 0.1, cable=cable1)
        self.system.add_edge('A','C', 20, 0.2, cable=cable2)
        self.system.add_edge('C','D', 30, 0.3, cable=cable3)
        self.system.add_edge('D','F', 40, 0.4, cable=cable1)
        self.system.add_edge('E','B', 50, 0.5, cable=cable2)
        self.system.add_edge('E','G', 60, 0.6, cable=cable3)
        self.system.add_edge('D','H', 110, 0.6, cable=cable1)

        self.system.update_vertex('A', weight=4)
        self.system.update_vertex('B', weight=8)
        self.system.update_vertex('C', weight=16)
        self.system.update_vertex('D', weight=32)
        self.system.update_vertex('E', weight=64)
        self.system.update_vertex('F', weight=128)
        self.system.update_vertex('G', weight=256)
        self.system.update_vertex('H', weight=512)
        #cargas = self.system.DFS_expert('A')
        cargas = self.system.accumulate_payload()

        value = {'A': 1340, 'B': 438, 'C': 868, 'D': 822, 'F': 128, 'E': 380, 'G': 256, 'H': 512}
        self.assertEqual(self.system.payload_list(), value)

        value = {
            'A': {'B': 0.1839561863946399, 'C': 0.49311221167439995},
            'B': {'E': 0.49311221167439995},
            'C': {'D': 0.03858115111818614},
            'D': {'F': 0.1839561863946399, 'H': 0.1839561863946399},
            'E': {'G': 0.03858115111818614},
            }
        self.system.k_factor_table()
        self.assertEqual(self.system.kfactor, value)

        value = {'A': {'\u039F': 0.0, 'B': 8.057280964085228, 'C': 85.60427994667583},
            'B': {'E': 93.69132021813598},
            'C': {'D': 9.514111865744702},
            'D': {'F': 9.418556743405563,'H': 56.511340460433374},
            'E': {'G': 5.926064811753391}
            }
        self.system.compute_drop_voltage_segment()
        self.assertEqual(self.system.drop_voltage_segment, value)

        value = {
            'A': 0.0,
            'B': 8.057280964085228,
            'E': 101.74860118222121,
            'G': 107.6746659939746,
            'C': 85.60427994667583,
            'D': 95.11839181242053,
            'F': 104.53694855582609,
            'H': 151.62973227285391,
            }
        self.system.DFS_drop_voltage()
        self.assertEqual(self.system.drop_voltage_accumulated, value)


if __name__ == '__main__':
    unittest.main()