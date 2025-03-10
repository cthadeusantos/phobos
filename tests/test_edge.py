import unittest
from source.cable import Cable
from source.edge import Edge

class TestEdge(unittest.TestCase):

    def test_edge_creation_with_cable(self):
        cable = Cable("Fiber Optic", 100)  # Create a Cable object
        edge = Edge(5, 15, cable=cable)
        self.assertEqual(edge.weight, 5)
        self.assertEqual(edge.distance, 15)
        self.assertEqual(edge.cable, cable)  # Check if the cable is correctly assigned

    def test_edge_creation_without_cable(self):
        edge = Edge(8, 20)  # No cable provided
        self.assertEqual(edge.weight, 8)
        self.assertEqual(edge.distance, 20)
        self.assertIsNone(edge.cable)  # Cable should be None

    def test_edge_string_representation_with_cable(self):
        cable = Cable("Copper", 50)
        edge = Edge(10, 25, cable=cable)
        expected_string = f"Edge: weight=10.0, distance=25.0, cable={cable}"
        self.assertEqual(str(edge), expected_string)

    def test_edge_string_representation_without_cable(self):
        edge = Edge(12, 30)
        self.assertEqual(str(edge), "Edge: weight=12.0, distance=30.0, cable=None")

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

    def test_distance_setter(self):
        edge = Edge()
        edge.distance = 10
        self.assertIsInstance(edge.distance, float)
        self.assertEqual(edge.distance, 10.0)
        
        edge.distance = 3.14159
        self.assertIsInstance(edge.distance, float)
        self.assertEqual(edge.distance, 3.14159)
        with self.assertRaises(TypeError):
            edge.distance = "abc"  # Tentativa de atribuir uma string não numérica
        with self.assertRaises(ValueError):
            edge.distance = -5  # Tentativa de atribuir um valor negativo

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