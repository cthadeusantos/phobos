import unittest
from source.graph import Graph  
from source.vertex import Vertex  
from source.edge import Edge  
from source.cable import Cable 

class TestGraph(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()
        self.v1 = Vertex("A", 10)
        self.v2 = Vertex("B", 20)
        self.v3 = Vertex("C", 30)
        self.cable1 = Cable("Fiber", 100)
        self.cable2 = Cable("Copper", 50)
        self.graph.addVertex(self.v1)
        self.graph.addVertex(self.v2)
        self.graph.addVertex(self.v3)

    def test_add_vertex(self):
        self.assertIn("A", self.graph.vertices)
        self.assertIn("B", self.graph.vertices)
        self.assertIn("C", self.graph.vertices)

    def test_add_edge(self):
        self.graph.add_edge("A", "B", 5, 15, self.cable1)
        self.graph.add_edge("A", "C", 15, 25, self.cable1)
        self.assertIn(self.v2, self.v1.get_neighbors_objects())
        self.assertIn(self.v1, self.v2.neighbors)
        self.assertEqual(self.v1.neighbors[self.v2].weight, 5)
        self.assertEqual(self.v1.neighbors[self.v2].distance, 15)
        self.assertEqual(self.v1.neighbors[self.v2].cable, self.cable1)

    # def test_add_edge_invalid_vertex(self):
    #     with self.assertRaises(AttributeError):  # Or KeyError, depending on your implementation
    #         self.graph.add_edge("A", "D", 5, 15, self.cable1)

#     def test_graph_string_representation(self):
#         self.graph.add_edge("A", "B", 5, 15, self.cable1)
#         expected_string = """Vertex: A (Weight: 10)
# -> Vertex: B (Weight: 20): Edge: weight=5, distance=15, cable=Cable: Type=Fiber, resistance=100
# Vertex: B (Weight: 20)
# -> Vertex: A (Weight: 10): Edge: weight=5, distance=15, cable=Cable: Type=Fiber, resistance=100
# Vertex: C (Weight: 30)"""  # Improved expected string
#         self.assertEqual(str(self.graph), expected_string)

    def test_add_edge_existing_edge(self):
        self.graph.add_edge("A", "B", 5, 15, self.cable1)
        self.graph.add_edge("A", "B", 8, 20, self.cable2) # Add another edge between A and B
        self.assertEqual(self.v1.neighbors[self.v2].weight, 8) # Check if the edge was updated
        self.assertEqual(self.v1.neighbors[self.v2].distance, 20) # Check if the edge was updated
        self.assertEqual(self.v1.neighbors[self.v2].cable, self.cable2) # Check if the edge was updated

    def test_has_edge_method(self):
        self.graph.add_edge("A", "B", 5, 15, self.cable1)
        self.graph.add_edge("A", "C", 15, 25, self.cable2)
        self.graph.add_edge("A", "D", 15, 25, self.cable1)
        self.graph.add_edge("D", "E", 35, 45, self.cable2)
        self.assertTrue(self.graph.has_edge('A', 'B'))
        self.assertTrue(self.graph.has_edge('A', 'C'))
        self.assertTrue(self.graph.has_edge('A', 'D'))
        self.assertTrue(self.graph.has_edge('D', 'E'))

    def test_add_edge_invalid_vertex(self):
        with self.assertRaises(AttributeError):  # Or KeyError, depending on your implementation
            self.graph.has_edge("A", "X")

    # def test_invalid_vertex(self):    
    #     with self.assertRaises(AttributeError):  # Or KeyError, depending on your implementation
    #         self.graph.tag_adjacency_vertex_list()

    def test_get_definitions(self):
        self.graph.add_edge("A", "B", 5, 15, self.cable1)
        self.graph.add_edge("A", "C", 15, 25, self.cable2)
        self.assertEqual(self.graph.get_num_vertices(), 3)
        self.assertEqual(self.graph.get_num_edges(), 2)

    def test_remove_vertex_and_edge(self):
        # Setting
        self.graph.add_edge("A", "B", 5, 15, self.cable1)
        self.graph.add_edge("A", "C", 6, 16, self.cable2)
        self.graph.add_edge("B", "C", 7, 17, self.cable2)
        self.graph.add_edge("D", "C", 8, 18, self.cable2)
        self.graph.add_edge("G", "C", 9, 19, self.cable2)

        # Testing
        self.graph.remove_vertex('A')
        self.assertEqual(self.graph.tag_adjacency_vertex_list(), ['B', 'C', 'D', 'G'])
        self.assertEqual(self.graph.get_num_edges(), 3)

        with self.assertRaises(AttributeError):  # Or KeyError, depending on your implementation
            self.graph.remove_vertex('X')

        with self.assertRaises(ValueError):
            self.graph.remove_edge('X', 'D')
            self.graph.remove_edge('D')

        self.graph.remove_edge('C', 'D')
        self.assertEqual(self.graph.get_num_edges(), 2)



if __name__ == '__main__':
    unittest.main()