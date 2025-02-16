import unittest
from source.vertex import Vertex
from source.edge import Edge


class TestVertex(unittest.TestCase):

    def setUp(self):  # Good practice to set up a vertex for testing
        self.vertex = Vertex("A", 10)

    def test_vertex_creation(self):
        self.assertEqual(self.vertex.tag, "A")
        self.assertEqual(self.vertex.weight, 10)
        self.assertEqual(self.vertex.neighbors, {})  # Initially empty

    def test_add_edge(self):
        other_vertex = Vertex("B", 20)  # Create another vertex
        other_vertex1 = Vertex("C", 25)  # Create another vertex
        edge = Edge(5, 15)  # Create an edge (you'll need an Edge class)
        edge1 = Edge(15, 25)  # Create an edge (you'll need an Edge class)
        self.vertex.add_edge(other_vertex, edge)
        self.vertex.add_edge(other_vertex1, edge1)
        self.assertIn(other_vertex.tag, self.vertex.get_neighbors_tag()) # Check if neighbor exists
        self.assertIn(self.vertex.tag, other_vertex.get_neighbors_tag()) # Check if neighbor exists
        self.assertEqual(self.vertex.get_edge(other_vertex), edge) # Check if edge is correct

    def test_vertex_string_representation(self):
        self.assertEqual(str(self.vertex), "Vertex: A (Weight: 10)")

    def test_add_edge_existing_neighbor(self):
        other_vertex = Vertex("B", 20)
        other_vertex2 = Vertex("C", 20)
        edge1 = Edge(5, 15)
        edge2 = Edge(8, 20)
        self.vertex.add_edge(other_vertex, edge1)
        self.vertex.add_edge(other_vertex, edge2)  # Add another edge to the same neighbor
        self.vertex.add_edge(other_vertex2, edge1)
        self.assertEqual(self.vertex.get_edge(other_vertex), edge2)  # Should overwrite the old edge
        self.assertIn(edge2, other_vertex.get_edges())
        self.assertIn(edge1, self.vertex.get_edges())
        self.assertNotIn(edge1, other_vertex.get_edges())

    def test_add_edge_invalid_input(self):
        with self.assertRaises(TypeError):
            self.vertex.add_edge("Not a vertex", "Not an edge")


if __name__ == '__main__':
    unittest.main()