from collections import defaultdict
from queue import Queue

from source.edge import Edge
from source.vertex import Vertex

class Graph:
    def __init__(self):
        self.vertices = {}  # Dicionário para armazenar vértices

    def addVertex(self, vertex=None):
        """Add a vertex to the graph.

        Returns:
            None
        """
        if vertex is not None and not isinstance(vertex, Vertex):
            raise TypeError("Invalid input!")
        vertex = vertex or Vertex()
        self.vertices[vertex.tag] = vertex

    def add_edge(self, source, target, weight=0, distance=0, cable=None):
        """Add an edge to the graph.

        Returns:
            None
        """
        edge = Edge(weight, distance, cable=cable)
        if source in self.vertices and target in self.vertices:
            self.vertices[source].add_edge(self.vertices[target], edge)
            self.vertices[target].add_edge(self.vertices[source], edge)
        else:
            if source not in self.vertices: # If source not exists , add it
                self.addVertex(Vertex(source))
                self.vertices[source].add_edge(self.vertices[target], edge)
                self.vertices[target].add_edge(self.vertices[source], edge)
            elif target not in self.vertices: # If target not exists, add it
                self.addVertex(Vertex(target))
                self.vertices[source].add_edge(self.vertices[target], edge)
                self.vertices[target].add_edge(self.vertices[source], edge)
            # else:
            #     raise AttributeError("Vertice(s) not found.")

    # def adjacency_vertex_list(self, source=None):
    #     #return [neighbor for neighbor in self.vertices[source].neighbors]
    #     if source is not None:
    #         return list(self.vertices[source].neighbors.keys())
    #     else:
    #         raise AttributeError("Vertice(s) not found.")
        
    def tag_adjacency_vertex_list(self, source=None):
        """Get the adjacency list from graph.

        Returns:
            a list: all vertices connected at source vertex
        """
        if source is not None:
            try: 
                return [object.tag for object in self.vertices[source].neighbors.keys()]
            except KeyError:
                raise AttributeError("Vertice(s) not found.")
        return [tag for tag in self.vertices.keys()]
    
    def object_adjacency_vertex_list(self, source=None):
        """Get the adjacency list from graph.

        Returns:
            a list: all vertices connected at source vertex
        """
        if source is not None:
            try: 
                return [object for object in self.vertices[source].neighbors.keys()]
            except KeyError:
                raise AttributeError("Vertice(s) not found.")
        return [tag for tag in self.vertices.keys()]

    
    # def adjacency_list(self):
    #     adjacency_list = {}
    #     for vertex in list(self.vertices.keys()):
    #         adjacency_list[vertex] = self.adjacency_vertex_list(vertex)
    #     return adjacency_list

    def has_edge(self, source, target):
        """Check if there is an edge between vertices source and target at graph.

        Returns:
            boolean: There is an edge (true) or There is not an edge (false)
        """
        return source in self.tag_adjacency_vertex_list(target) and target in self.tag_adjacency_vertex_list(source)

    def get_num_vertices(self):
        """Calculates the total number of vertices in the graph.

        Returns:
            int: The total number of vertices.
        """
        return len(self.vertices)
    
    def get_num_edges(self):
        """Calculates the total number of edges in the graph.

        Returns:
            int: The total number of edges.
        """
        return sum(vertex.get_num_edges(vertex_id) for vertex_id, vertex in self.vertices.items()) // 2

    # def get_edges(self, source=None):
    #     if source is not None:
    #         for vertex, edge in self.vertices[source].neighbors.items():
    #             self.remove_edge(vertex.tag, source)
    #     pass


    def remove_vertex(self, source=None):
        if source is None:
            raise AttributeError("Invalid vertex!")
        
        tag_vertex_list = self.tag_adjacency_vertex_list(source)
        instance_source = self.vertices[source]
        for tag in tag_vertex_list:
            self.vertices[tag].neighbors.pop(instance_source, None)
        self.vertices.pop(source, None)

    # def remove_edge(self, source, target):
    #     if source is None or target is None or source not in self.tag_adjacency_vertex_list() or target not in self.tag_adjacency_vertex_list():
    #         raise AttributeError("Invalid vertice(s)!")
    #     instance_source = self.vertices[source]
    #     instance_target = self.vertices[target]
    #     self.vertices[source].neighbors.pop(instance_target, None)
    #     self.vertices[target].neighbors.pop(instance_source, None)

    def remove_edge(self, source, target):
        """Removes an edge between two vertices.

        Args:
            source: The tag of the source vertex.
            target: The tag of the target vertex.

        Raises:
            ValueError: If either vertex tag is invalid.
        """

        if source is None or target is None:
            raise ValueError("Vertex tags cannot be None.")

        if source not in self.vertices or target not in self.vertices:
            raise ValueError("Invalid vertex tag(s).")

        self.vertices[source].neighbors.pop(self.vertices[target], None)
        self.vertices[target].neighbors.pop(self.vertices[source], None)

    def __str__(self):
        grafo_str = ""
        for vertice in self.vertices.values():
            grafo_str += str(vertice) + "\n"
            for neighbor, edge in vertice.neighbors.items():
                grafo_str += f"  -> {neighbor}: {edge}\n"
        return grafo_str

# # This class represents a undirect graph
# # using adjacency list
# class Graph:

#     """
#     Constructor
#     """
#     def __init__(self):

#         # Default dictionary to store a graph
#         self.graph = defaultdict(list)

#     """
#     Add an edge to graph
#     """
#     def add_edge(self, u, v, **kwargs):
#         if not self.has_edge(u, v):
#             self.graph[u].append(v)
#             self.graph[v].append(u)

#     def removeEdge(self, u, v):
#         if self.has_edge(u, v) and self.has_edge(v, u):
#             self.graph[u].remove(v)
#             self.graph[v].remove(u)
    
#     # def removeVertex(self,u):
#     #     for v in self.graph[u]:
#     #         self.removeEdge(u, v)
#     #     del self.graph[u]

#     def has_edge(self, u, v):
#         return v in self.graph[u] and u in self.graph[v]
    
#     def getNumVertices(self):
#         return max(self.graph)

#     def elements(self):
#         return max(self.graph)

#     def __str__(self):
#         string = ''
#         for x in self.graph:
#             string += f'{x}:{self.graph[x]}\n'
#         return string

#     def BFS(self, start):
        
#         visited = [False] * (max(self.graph) + 1)   # Mark all vertices as not visited
        
#         queue = Queue() # Create queue for BFS

#         queue.put(start)
#         visited[start] = True
#         while not queue.empty():
#             start = queue.get()
#             print(start, end=" ")
#             for i in self.graph[start]:
#                 if not visited[i]:
#                     queue.put(i)
#                     visited[i] =  True

#     # def DFS(self, start):
#     #     visited = [False] * (max(self.graph) + 1)
#     #     stack = []  # Use a list as a stack

#     #     stack.append(start)  # Use append() to push onto the stack

#     #     while stack:
#     #         start = stack.pop()  # Use pop() to pop from the stack

#     #         if not visited[start]:
#     #             print(start, end=" ")
#     #             visited[start] = True

#     #             # Note: Reverse the order of neighbors to maintain DFS order
#     #             for neighbor in reversed(self.graph[start]):  # Corrected this line
#     #                 if not visited[neighbor]:
#     #                     stack.append(neighbor)

#     def DFS(self, start, visited=None):
#         if visited is None:
#             visited = set()
#         visited.add(start)
#         #print(start, end=" ")

#         for neighbor in self.graph[start]:
#             if neighbor not in visited:
#                 self.DFS(neighbor, visited)
