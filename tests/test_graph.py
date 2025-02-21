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
        self.v3 = Vertex("C", 30.2)
        self.cable1 = Cable("Fiber", 100)
        self.cable2 = Cable("Copper", 50)
        self.graph.add_vertex(self.v1)
        self.graph.add_vertex(self.v2)
        self.graph.add_vertex(self.v3)

    def test_get_weight(self):
        self.assertEqual(self.v1.get_weight(), 10)
        self.assertEqual(self.v2.get_weight(), 20)
        self.assertEqual(self.v3.get_weight(), 30.2)

    def test_get_edge_weight(self):
        self.graph.add_edge("D", "B", 50, 15.7, self.cable1)
        self.graph.add_edge("E", "C", 15.8, 25.8, self.cable1)
        self.assertEqual(self.graph.get_edge_weight('B', 'D'), 50)
        self.assertEqual(self.graph.get_edge_weight('C', 'E'), 15.8)

    def test_get_distance(self):
        self.graph.add_edge("A", "B", 50, 15.7, self.cable1)
        self.graph.add_edge("A", "C", 15.8, 25.8, self.cable1)
        self.assertEqual(self.graph.get_distance('A', 'B'), 15.7)
        self.assertEqual(self.graph.get_distance('A', 'C'), 25.8)

    def test_coordinates(self):
        self.graph.add_edge("A", "B", 50, 15.7, self.cable1)
        self.graph.add_edge("A", "C", 15.8, 25.8, self.cable1)
        self.assertEqual(self.graph.get_distance('A', 'B'), 15.7)
        self.assertEqual(self.graph.get_distance('A', 'C'), 25.8)

    def test_add_vertex(self):
        self.assertIn("A", self.graph.vertices)
        self.assertIn("B", self.graph.vertices)
        self.assertIn("C", self.graph.vertices)
        self.graph.add_vertex("X", 40)
        self.assertEqual(self.graph.get_vertex_weight('X'), 40)

        with self.assertRaises(ValueError):
            self.graph.add_vertex(self.v1)
        with self.assertRaises(ValueError):
            self.graph.add_vertex("X", -40)

    def test_add_edge(self):
        self.graph.add_edge("A", "B", 5, 15, self.cable1)
        self.graph.add_edge("A", "C", 15, 25, self.cable1)
        self.assertIn(self.v2, self.v1.get_neighbors_objects())
        self.assertIn(self.v1, self.v2.neighbors)
        self.assertEqual(self.v1.neighbors[self.v2].weight, 5)
        self.assertEqual(self.v1.neighbors[self.v2].distance, 15)
        self.assertEqual(self.v1.neighbors[self.v2].cable, self.cable1)

    def test_update_edge(self):
        self.graph.add_edge("A", "B", 5, 15, self.cable1)
        self.graph.update_edge("A", "B", 15, 25, self.cable1)
        self.assertEqual(self.v1.neighbors[self.v2].weight, 15)
        self.assertEqual(self.graph.get_edge_weight('A', 'B'), 15)
        self.assertEqual(self.v1.neighbors[self.v2].distance, 25)
        self.assertEqual(self.v1.neighbors[self.v2].cable, self.cable1)

    def test_add_invalid_edge(self):
        with self.assertRaises(AttributeError):
            self.graph.add_edge(distance=5, weight=15, cable=self.cable1)

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

    def test_bfs_and_dfs(self):
        self.v4 = Vertex("D", 40)
        self.v5 = Vertex("E", 50)
        self.v6 = Vertex("F", 60)
        self.v7 = Vertex("G", 60)
        self.v8 = Vertex("H", 60)
        self.graph.add_vertex(self.v4)
        self.graph.add_vertex(self.v5)
        self.graph.add_vertex(self.v6)
        self.graph.add_vertex(self.v7)
        self.graph.add_edge("A", "B", 5, 15, self.cable1)
        self.graph.add_edge("A", "C", 6, 16, self.cable2)
        self.graph.add_edge("C", "D", 7, 17, self.cable2)
        self.graph.add_edge("D", "E", 8, 18, self.cable2)
        self.graph.add_edge("B", "F", 9, 19, self.cable2)
        self.graph.add_edge("F", "G", 9, 19, self.cable2)
        self.graph.add_edge("B", "H", 9, 19, self.cable2)

        self.assertEqual(self.graph.BFS('A'), ['A', 'B', 'C', 'F', 'H', 'D', 'G', 'E'])
        self.assertEqual(self.graph.DFS('A'), ['A', 'B', 'F', 'G', 'H', 'C', 'D', 'E'])

    def test_rename_vertex(self):
        self.graph.add_edge("A", "B", 5, 15, self.cable1)
        self.graph.add_edge("A", "C", 6, 16, self.cable2)
        self.graph.rename_vertex('A', 'Z')
        self.assertEqual(self.graph.tag_adjacency_vertex_list(), ['B', 'C', 'Z'])

        with self.assertRaises(ValueError):
            self.graph.rename_vertex('X')
            self.graph.rename_vertex('Z', 'F')
            self.graph.rename_vertex('A', 'B')

        with self.assertRaises(TypeError):
            self.graph.rename_vertex('A', Vertex)

    def test_update_vertex(self):
        self.graph.add_edge("A", "B", 5, 15, self.cable1)
        self.graph.add_edge("A", "C", 6, 16, self.cable2)
        self.graph.update_vertex('A', 100)
        self.assertEqual(self.graph.get_vertex_weight('A'), 100)

        with self.assertRaises(ValueError):
            self.graph.update_vertex('X', 100)

        with self.assertRaises(TypeError):
            self.graph.update_vertex('A', '100')

        with self.assertRaises(ValueError):
            self.graph.update_vertex()

if __name__ == '__main__':
    unittest.main()