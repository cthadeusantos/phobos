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

if __name__ == '__main__':
    unittest.main()