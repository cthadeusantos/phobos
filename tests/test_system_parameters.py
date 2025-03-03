import unittest

from source.system import System
from source.vertex import Vertex
from source.database import CableDBMT
from source.cable import Cable
from source.fileio import FileIO

class TestSystem(unittest.TestCase):

    def setUp(self):
        self.system = System()
        self.file = FileIO()
        self.cable_db = CableDBMT('databases/mt.db')

        self.cable1 = Cable()
        self.cable1.setting(self.cable_db.get_cable_especifications(id=180, installation=1))
        self.cable2 = Cable()
        self.cable2.setting(self.cable_db.get_cable_especifications(id=150, installation=0))
        self.cable3 = Cable()
        self.cable3.setting(self.cable_db.get_cable_especifications(id=88, installation=0))
        pass

    def test_insert_parameters(self):
        data = { 'root': '1', 'vline': 220, 'vphase': 127, 'power_factor': 0.5 }
        phobos = System(data=data)
        self.assertEqual(phobos.get_setup(), {'root': '1', 'vline': 220, 'vphase': 127, 'power_factor': 0.5})

        phobos = System(root='10', vline=125, vphase=96, power_factor=0.8)
        self.assertEqual(phobos.get_setup(), {'root': '10', 'vline': 125, 'vphase': 96, 'power_factor': 0.8})

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

    def test_vline(self):
        self.system.vline = 220
        self.assertIsInstance(self.system.vline, int)
        self.assertEqual(self.system.vline, 220)
        self.system.vline = 127.5
        self.assertIsInstance(self.system.vline, float)
        self.assertEqual(self.system.vline, 127.5)
        
        with self.assertRaises(ValueError):
            self.system.vline = -6.3  # Tentativa de atribuir um valor negativo
        with self.assertRaises(TypeError):
            self.system.vphase = (1,4)  # Tentativa de atribuir um tipo invalido
            
    def test_vphase(self):
        self.system.vphase = 220
        self.assertIsInstance(self.system.vphase, int)
        self.assertEqual(self.system.vphase, 220)
        self.system.vphase = 127.5
        self.assertIsInstance(self.system.vphase, float)
        self.assertEqual(self.system.vphase, 127.5)
        
        with self.assertRaises(ValueError):
            self.system.vphase = -6.3  # Tentativa de atribuir um valor negativo
        with self.assertRaises(TypeError):
            self.system.vphase = (1,4)  # Tentativa de atribuir um tipo invalido

        self.system.add_edge('A','B', 0, 10)
        self.system.add_edge('A','C', 0, 20)
        self.system.add_edge('C','D', 0, 30)
        self.system.add_edge('D','F', 0, 40)
        self.system.add_edge('E','B', 0, 50)
        self.system.add_edge('E','G', 0, 60)

    def test_DFS_expert(self):
        self.system.reset()
        self.system.add_edge('A','B', 10, 10, distributed=1)
        self.system.add_edge('A','C', 20, 20, distributed=1)
        self.system.add_edge('C','D', 30, 30, distributed=1)
        self.system.add_edge('D','F', 40, 40, distributed=1)
        self.system.add_edge('E','B', 50, 50, distributed=1)
        self.system.add_edge('E','G', 60, 60, distributed=1)
        self.system.add_edge('D','H', 110, 60, distributed=1)

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
        self.assertEqual(self.system.get_segment_payload_all(), {'G': {'E': 286}, 'E': {'B': 405}, 'B': {'A': 443}, 'H': {'D': 567}, 'F': {'D': 148}, 'D': {'C': 837}, 'C': {'A': 878}})

    def test_kfactor(self):
        self.system.reset()

        # cable1 = Cable()
        # cable1.setting(self.cable_db.get_cable_especifications(id=180, installation=1))
        # cable2 = Cable()
        # cable2.setting(self.cable_db.get_cable_especifications(id=150, installation=0))
        # cable3 = Cable()
        # cable3.setting(self.cable_db.get_cable_especifications(id=88, installation=0))

        self.system.vline=13.8
        self.system.vphase=13.8
        self.system.power_factor=0.9
        self.system.root='A'

        self.system.set_vn(self.system.vline)

        self.system.add_edge('A','B', 10, 0.1, cable=self.cable1, distributed=1)
        self.system.add_edge('A','C', 20, 0.2, cable=self.cable2, distributed=1)
        self.system.add_edge('C','D', 30, 0.3, cable=self.cable3, distributed=1)
        self.system.add_edge('D','F', 40, 0.4, cable=self.cable1, distributed=1)
        self.system.add_edge('E','B', 50, 0.5, cable=self.cable2, distributed=1)
        self.system.add_edge('E','G', 60, 0.6, cable=self.cable3, distributed=1)
        self.system.add_edge('D','H', 110, 0.6, cable=self.cable1, distributed=1)

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

        value = {'A': {'\u039F': 0.0, 'B': 8.149259057282547, 'C': 86.59050437002463},
            'B': {'E': 99.855222864066},
            'C': {'D': 9.68772704577654},
            'D': {'F': 10.890206234562683,'H': 62.58189461145649},
            'E': {'G': 6.620525531880742}
            }
        self.system.compute_drop_voltage_segment()
        self.assertEqual(self.system.drop_voltage_segment, value)

        value = {
            'A': 0.0,
            'B': 8.149259057282547,
            'E': 108.00448192134854,
            'G': 114.62500745322929,
            'C': 86.59050437002463,
            'D': 96.27823141580117,
            'F': 107.16843765036386,
            'H': 158.86012602725765,
            }
        self.system.DFS_drop_voltage()
        self.assertEqual(self.system.drop_voltage_accumulated, value)


if __name__ == '__main__':
    unittest.main()