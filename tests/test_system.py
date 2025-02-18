import unittest

from source.system import System
from source.vertex import Vertex

class TestSystem(unittest.TestCase):

    def test_root_setter(self):
        system = System()
        system.root = 10
        self.assertIsInstance(system.root, int)
        self.assertEqual(system.root, 10)

        system.root = "A"
        self.assertIsInstance(system.root, str)
        self.assertEqual(system.root, 'A')
        
        with self.assertRaises(TypeError):
            system.root = Vertex()  # Tentativa de atribuir uma string não numérica
        with self.assertRaises(ValueError):
            system.root = -5  # Tentativa de atribuir um valor negativo