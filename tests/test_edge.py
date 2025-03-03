import unittest
from source.cable import Cable
from source.edge import Edge
from source.database import CableDBMT

class TestEdge(unittest.TestCase):

    def test_edge_creation(self):
        edge = Edge(5, 15)
        self.assertEqual(edge.weight, 5)
        self.assertEqual(edge.distance, 15)

    def test_edge_string(self):
        edge = Edge(10, 25)
        expected_string = f"Edge: weight=10.0, distance=25.0"
        self.assertEqual(str(edge), expected_string)

    def test_weight_setter(self):
        edge = Edge()
        edge.weight = 10
        self.assertIsInstance(edge.weight, float)
        self.assertEqual(edge.weight, 10.0)
        
        edge.weight = 3.14159
        self.assertIsInstance(edge.weight, float)
        self.assertEqual(edge.weight, 3.14159)
        with self.assertRaises(TypeError):
            edge.weight = "abc"  # Tentativa de atribuir uma string não numérica
        with self.assertRaises(ValueError):
            edge.weight = -5  # Tentativa de atribuir um valor negativo

    def test_edge_invalid_input(self):
        with self.assertRaises(TypeError):
            Edge("not a number", 15)
        with self.assertRaises(TypeError):
            Edge(5, "not a number")
        with self.assertRaises(ValueError):
            Edge(-1, 15) # Weight should not be negative
        with self.assertRaises(ValueError):
            Edge(5, -1) # distance should not be negative

if __name__ == '__main__':
    unittest.main()