import unittest

from source.system import System
from source.vertex import Vertex

class TestSystem(unittest.TestCase):

    def setUp(self):
        #return super().setUp()
        self.system = System()
        #self.system2 = System()

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
            self.system.add_edge('A','B', 10, 20, coord_source=(5, 7), coord_target=(10, 9))

    def test_update_edge(self):
        self.system.add_edge('A','B', 10, 20, coord_source=(5, 7), coord_target=(10, 9))
        self.system.update_edge('A','B', 20, 30, coord_source=(5, 7), coord_target=(10, 9))
        self.assertEqual(self.system.get_coordinates('A'), (5, 7))
        self.assertEqual(self.system.get_coordinates('B'), (10, 9))
        self.assertEqual(self.system.get_edge_weight('A', 'B'), 20)

        with self.assertRaises(ValueError):
            self.system.update_edge('A','C', 20, 30, coord_source=(5, 7), coord_target=(10, 9))

        with self.assertRaises(TypeError):
            self.system.update_edge('A','B', 20, 30, coord_source=Vertex(), coord_target=(10, 9))

        with self.assertRaises(TypeError):
            self.system.update_edge('A','B', 20, 30, coord_source=(10, 9), coord_target=Vertex())

        with self.assertRaises(TypeError):
            self.system.update_edge('A','B', 20, 30, coord_source=("10", 9), coord_target=(5,7))

        with self.assertRaises(TypeError):
            self.system.update_edge('A','B', 20, 30, coord_source=(10, 9), coord_target=(5,'7'))
    
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

        # self.system.add_edge('A','B', 0, 10)
        # self.system.add_edge('A','C', 0, 20)
        # self.system.add_edge('C','D', 0, 30)
        # self.system.add_edge('D','F', 0, 40)
        # self.system.add_edge('E','B', 0, 50)
        # self.system.add_edge('E','G', 0, 60)

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
