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
        expected_string = f"Edge: weight=10, distance=25, cable={cable}"
        self.assertEqual(str(edge), expected_string)

    def test_edge_string_representation_without_cable(self):
        edge = Edge(12, 30)
        self.assertEqual(str(edge), "Edge: weight=12, distance=30, cable=None")

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