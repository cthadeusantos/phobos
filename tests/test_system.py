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

    def test_add_vertex(self):
        vertex1 = self.system.add_vertex('A', 0, (1, 2), 3)
        vertex2 = self.system.add_vertex('B', 5, (6, 7), 8)

        self.assertEqual(self.system.get_vertex_weight('A'), 0)
        self.assertEqual(self.system.get_coordinates('A'), (1, 2))
        self.assertEqual(self.system.get_payload('A'), 3)
        self.assertEqual(self.system.get_vertex_weight('B'), 5)
        self.assertEqual(self.system.get_coordinates('B'), (6,7))
        self.assertEqual(self.system.get_payload('B'), 8)

        with self.assertRaises(TypeError):
            self.system.add_vertex('C', 0, (0, Vertex()), 3)  # Tentativa de atribuir uma string não numérica
        with self.assertRaises(TypeError):
            self.system.add_vertex('D', (0, Vertex()), 0, 3)  # Tentativa de atribuir uma string não numérica
        with self.assertRaises(TypeError):
            self.system.add_vertex('E', 0, (0, 0), Vertex())  # Tentativa de atribuir uma string não numérica
        with self.assertRaises(ValueError):
            self.system.add_vertex('F', 0, (0, 0), -1)  # tentativa de atribuir um número negativo a payload

    def test_update_vertex(self):
        self.system.add_vertex('Z', 10, (1, 2), 3)
        self.system.update_vertex('Z', coordinates=(5, 10), payload=15, weight=20)
        self.assertEqual(self.system.get_coordinates('Z'), (5, 10))
        self.assertEqual(self.system.get_payload('Z'), 15)
        self.assertEqual(self.system.get_vertex_weight('Z'), 20)
        with self.assertRaises(ValueError):
            self.system.update_vertex('W', coordinates=(5, 10), payload=15, weight=20)
        with self.assertRaises(ValueError):
            self.system.update_vertex(coordinates=(5, 10), payload=15, weight=20)
        with self.assertRaises(ValueError):
            self.system.update_vertex('Z', coordinates=(5, 10), payload=-15, weight=20)
        with self.assertRaises(ValueError):
            self.system.update_vertex('Z', coordinates=(5, 10), payload=15, weight=-20)
        with self.assertRaises(TypeError):
            self.system.update_vertex(Vertex(), coordinates=(5, 10), payload=15, weight=20)

    def test_add_edge(self):
        # self.system.add_edge('A','B', 0, 10)
        self.system.add_edge('A','B', 10, 20, coord_source=(5, 7), coord_target=(10, 9))
        self.assertEqual(self.system.get_coordinates('A'), (5, 7))
        self.assertEqual(self.system.get_coordinates('B'), (10, 9))
        self.assertEqual(self.system.get_edge_weight('A', 'B'), 10)

        with self.assertRaises(ValueError): # Tentativa de adicionar uma aresta já existente
            self.system.add_edge('A','B', 10, 20, coord_source=(5, 7), coord_target=(10, 9), overlap=False)

    def test_update_edge(self):
        cable = Cable()
        self.system.add_edge('A','B', 10, 20, cable, coord_source=(5, 7), coord_target=(10, 9))
        self.system.update_edge('A','B', 20, 30, cable, coord_source=(5, 7), coord_target=(10, 9))
        self.assertEqual(self.system.get_coordinates('A'), (5, 7))
        self.assertEqual(self.system.get_coordinates('B'), (10, 9))
        self.assertEqual(self.system.get_edge_weight('A', 'B'), 20)

        with self.assertRaises(ValueError):
            self.system.update_edge('A','C', 20, 30, cable, coord_source=(5, 7), coord_target=(10, 9))

        with self.assertRaises(TypeError):
            self.system.update_edge('A','B', 20, 30, cable, coord_source=Vertex(), coord_target=(10, 9))

        with self.assertRaises(TypeError):
            self.system.update_edge('A','B', 20, 30, cable, coord_source=(10, 9), coord_target=Vertex())

        with self.assertRaises(TypeError):
            self.system.update_edge('A','B', 20, 30, cable, coord_source=("10", 9), coord_target=(5,7))

        with self.assertRaises(TypeError):
            self.system.update_edge('A','B', 20, 30, cable, coord_source=(10, 9), coord_target=(5,'7'))
    
    def test_reset(self):
        self.system = self.system.reset()
        self.assertEqual(self.system.vertices, {})

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
        #cargas = self.system.DFS_expert('A')
        cargas = self.system.accumulate_payload('A')
        self.assertEqual(cargas, {'A': 1340, 'B': 438, 'C': 868, 'D': 822, 'F': 128, 'E': 380, 'G': 256, 'H': 512})   

    # def test_build_tree(self):
    #     self.assertEqual(self.system.adjacency_list(),{'A': ['B', 'C'], 'B': ['A', 'E'], 'C': ['A', 'D'], 'D': ['C', 'F'], 'F': ['D'], 'E': ['B', 'G'], 'G': ['E']})
    def test_save_file(self):
        data = { 'root': '1', 'vpp': 220, 'vpn': 127, 'power_factor': 0.5 }
        
        phobos = System(data=data)

        phobos.add_vertex('A', 10)
        phobos.add_vertex('B', 11)
        phobos.add_vertex('C', 12)
        phobos.add_vertex('D', 14)
        phobos.add_vertex('E', 15)
        phobos.add_vertex('F', 16)
        phobos.add_vertex('G', 17)
        phobos.add_vertex('H', 18)
        phobos.add_vertex('I', 19)

        phobos.add_edge("A", "B")

        cable1 = Cable()
        cable1.setting(self.cable_db.get_cable_especifications(id=180, installation=2))
        cable2 = Cable()
        cable2.setting(self.cable_db.get_cable_especifications(id=150, installation=1))
        cable3 = Cable()
        cable3.setting(self.cable_db.get_cable_especifications(id=88, installation=0))

        phobos.update_edge('A','C', 21, 100, cable=cable1)
        phobos.update_edge('A','B', 22, 101, cable=cable1)
        phobos.update_edge('B','D', 23, 102, cable=cable2)
        phobos.update_edge('B','E', 24, 103, cable=cable2)
        phobos.update_edge('E','I', 25, 104, cable=cable1)
        phobos.update_edge('C','F', 26, 105, cable=cable3)
        phobos.update_edge('C','H', 26, 106, cable=cable3)
        phobos.update_edge('G','F', 28, 107, cable=cable3)

        data = phobos.serializeData()

        self.file.save(data, 'data/test.json')

        with open('data/test.json') as file:
            textfile = file.read()

        self.assertEqual(textfile, """{
    "graph": {
        "A": {
            "coordinate_x": 0,
            "coordinate_y": 0,
            "edges": {
                "B": {
                    "cable_id": 180,
                    "edge_distance": 101.0,
                    "edge_weight": 22.0,
                    "installation": 0
                },
                "C": {
                    "cable_id": 180,
                    "edge_distance": 100.0,
                    "edge_weight": 21.0,
                    "installation": 0
                }
            },
            "vertex_weight": 10.0
        },
        "B": {
            "coordinate_x": 0,
            "coordinate_y": 0,
            "edges": {
                "A": {
                    "cable_id": 180,
                    "edge_distance": 101.0,
                    "edge_weight": 22.0,
                    "installation": 0
                },
                "D": {
                    "cable_id": 150,
                    "edge_distance": 102.0,
                    "edge_weight": 23.0,
                    "installation": 0
                },
                "E": {
                    "cable_id": 150,
                    "edge_distance": 103.0,
                    "edge_weight": 24.0,
                    "installation": 0
                }
            },
            "vertex_weight": 11.0
        },
        "C": {
            "coordinate_x": 0,
            "coordinate_y": 0,
            "edges": {
                "A": {
                    "cable_id": 180,
                    "edge_distance": 100.0,
                    "edge_weight": 21.0,
                    "installation": 0
                },
                "F": {
                    "cable_id": 88,
                    "edge_distance": 105.0,
                    "edge_weight": 26.0,
                    "installation": 0
                },
                "H": {
                    "cable_id": 88,
                    "edge_distance": 106.0,
                    "edge_weight": 26.0,
                    "installation": 0
                }
            },
            "vertex_weight": 12.0
        },
        "D": {
            "coordinate_x": 0,
            "coordinate_y": 0,
            "edges": {
                "B": {
                    "cable_id": 150,
                    "edge_distance": 102.0,
                    "edge_weight": 23.0,
                    "installation": 0
                }
            },
            "vertex_weight": 14.0
        },
        "E": {
            "coordinate_x": 0,
            "coordinate_y": 0,
            "edges": {
                "B": {
                    "cable_id": 150,
                    "edge_distance": 103.0,
                    "edge_weight": 24.0,
                    "installation": 0
                },
                "I": {
                    "cable_id": 180,
                    "edge_distance": 104.0,
                    "edge_weight": 25.0,
                    "installation": 0
                }
            },
            "vertex_weight": 15.0
        },
        "F": {
            "coordinate_x": 0,
            "coordinate_y": 0,
            "edges": {
                "C": {
                    "cable_id": 88,
                    "edge_distance": 105.0,
                    "edge_weight": 26.0,
                    "installation": 0
                },
                "G": {
                    "cable_id": 88,
                    "edge_distance": 107.0,
                    "edge_weight": 28.0,
                    "installation": 0
                }
            },
            "vertex_weight": 16.0
        },
        "G": {
            "coordinate_x": 0,
            "coordinate_y": 0,
            "edges": {
                "F": {
                    "cable_id": 88,
                    "edge_distance": 107.0,
                    "edge_weight": 28.0,
                    "installation": 0
                }
            },
            "vertex_weight": 17.0
        },
        "H": {
            "coordinate_x": 0,
            "coordinate_y": 0,
            "edges": {
                "C": {
                    "cable_id": 88,
                    "edge_distance": 106.0,
                    "edge_weight": 26.0,
                    "installation": 0
                }
            },
            "vertex_weight": 18.0
        },
        "I": {
            "coordinate_x": 0,
            "coordinate_y": 0,
            "edges": {
                "E": {
                    "cable_id": 180,
                    "edge_distance": 104.0,
                    "edge_weight": 25.0,
                    "installation": 0
                }
            },
            "vertex_weight": 19.0
        }
    },
    "power_factor": 0.5,
    "root": "1",
    "vpn": 127,
    "vpp": 220
}""")

    def test_read_file(self):
        data = { 'root': '1', 'vpp': 220, 'vpn': 127, 'power_factor': 0.5 }
        phobos = System(data=data)
        data = self.file.read('data/entrada.json')
        cable_db = CableDBMT('databases/mt.db')
        phobos.deserializeData(data, database=cable_db)
        self.assertEqual(phobos.get_neighbors('C'), ['A', 'F', 'H'])
        self.assertEqual(phobos.get_edge_weight('I', 'E'), 25.0)

        x =  phobos.get_cable('A', 'C')

        self.assertEqual(phobos.get_cable('A','C').get_rcc(), 0.193)
        self.assertEqual(phobos.get_cable('A','C').get_xc(), 7.702)
        self.assertEqual(phobos.get_cable('A','C').get_rca(), 0.258)
        self.assertEqual(phobos.get_cable('A','C').get_xl(), 0.271)

        self.assertEqual(phobos.get_cable('B','D').get_rcc(), 0.727)
        self.assertEqual(phobos.get_cable('B','D').get_xc(), 10.739)
        self.assertEqual(phobos.get_cable('B','D').get_rca(), 0.933)
        self.assertEqual(phobos.get_cable('B','D').get_xl(), 0.228)

        self.assertEqual(phobos.get_cable('C','F').get_rcc(), 0.037)
        self.assertEqual(phobos.get_cable('C','F').get_xc(), 3.062)
        self.assertEqual(phobos.get_cable('C','F').get_rca(), 0.055)
        self.assertEqual(phobos.get_cable('C','F').get_xl(), 0.055)

        with self.assertRaises(ValueError):
            self.assertEqual(phobos.get_cable('Z','F').get_xl(), 0.055)
            self.assertEqual(phobos.get_cable('C','Z').get_xl(), 0.055)


    def test_insert_parameters(self):
        data = { 'root': '1', 'vpp': 220, 'vpn': 127, 'power_factor': 0.5 }
        phobos = System(data=data)
        self.assertEqual(phobos.get_setup(), {'root': '1', 'vpp': 220, 'vpn': 127, 'power_factor': 0.5})

        phobos = System(root='10', vpp=125, vpn=96, power_factor=0.8)
        self.assertEqual(phobos.get_setup(), {'root': '10', 'vpp': 125, 'vpn': 96, 'power_factor': 0.8})

if __name__ == '__main__':
    unittest.main()