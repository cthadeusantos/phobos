from collections import defaultdict
from queue import Queue
from collections import deque 

from source.edge import Edge
from source.vertex import Vertex



class Graph:

    class Sentinel:
            pass

    _SENTINEL = Sentinel()

    def __init__(self):
        """ Constructor

        Returns:
            None
        """
        self.vertices = {}  # Dicionário para armazenar vértices

    def get_vertex_weight(self, vertex):
        """Get the weight of a vertex.

        Args:
            vertex: The tag of the vertex.

        Returns:
            float: The weight of the vertex.
        """
        if not isinstance(vertex, (str, int)):
            raise TypeError("Invalid input!")
        return self.vertices[vertex].weight

    def get_distance(self, source=None, target=None):
        if source is None or target is None:
            raise ValueError("Vertex cannot be None")
        if source not in self.vertices or target not in self.vertices:
            raise ValueError("Vertex not found")
        if not isinstance(source, (str, int)) and not isinstance(target, (str, int)):
            raise TypeError("Invalid input!")
        instance = self.vertices[target]
        return self.vertices[source].neighbors[instance].distance

    def get_edge_weight(self, source=None, target=None):
        if source is None or target is None:
            raise ValueError("Vertex cannot be None")
        if source not in self.vertices or target not in self.vertices:
            raise ValueError("Vertex not found")
        if not isinstance(source, (str, int)) and not isinstance(target, (str, int)):
            raise TypeError("Invalid input!")
        instance = self.vertices[target]
        return self.vertices[source].neighbors[instance].weight

    def get_cable(self, source=None, target=None):
        if source is None or target is None:
            raise ValueError("Vertex cannot be None")
        if source not in self.vertices or target not in self.vertices:
            raise ValueError("Vertex not found")
        if not isinstance(source, (str, int)) and not isinstance(target, (str, int)):
            raise TypeError("Invalid input!")
        instance = self.vertices[target]
        return self.vertices[source].neighbors[instance].cable

    def add_vertex(self, vertex=None, weight=0):
        """Add a vertex to the graph.

        Returns:
            None
        """
        if vertex is not None and not isinstance(vertex, Vertex) and not isinstance(vertex, str) and not isinstance(vertex, int):
            raise TypeError("Invalid input!")
        if vertex is None:
            vertex = Vertex()
        elif isinstance(vertex, (str, int)):
            if vertex in self.vertices:
                raise ValueError("Vertex already exists!")
            vertex = Vertex(vertex, weight)
        elif isinstance(vertex, Vertex):
            if vertex.tag in self.vertices:
                raise ValueError("Vertex already exists!")
            vertex = vertex
        self.vertices[vertex.tag] = vertex

    def add_edge(self, source=None, target=None, weight=0, distance=0, cable=None):
        """Add an edge to the graph.

        Returns:
            None
        """
        if source is None or target is None:
            raise AttributeError("Invalid input!")
        edge = Edge(weight, distance, cable=cable)
        if source in self.vertices and target in self.vertices:
            self.vertices[source].add_edge(self.vertices[target], edge)
            self.vertices[target].add_edge(self.vertices[source], edge)
        else:
            if source not in self.vertices and target not in self.vertices: # If source not exists , add it
                self.add_vertex(Vertex(source))
                self.add_vertex(Vertex(target))
                self.vertices[source].add_edge(self.vertices[target], edge)
                self.vertices[target].add_edge(self.vertices[source], edge)
            elif source not in self.vertices: # If source not exists , add it
                self.add_vertex(Vertex(source))
                self.vertices[source].add_edge(self.vertices[target], edge)
                self.vertices[target].add_edge(self.vertices[source], edge)
            elif target not in self.vertices: # If target not exists, add it
                self.add_vertex(Vertex(target))
                self.vertices[source].add_edge(self.vertices[target], edge)
                self.vertices[target].add_edge(self.vertices[source], edge)

    def update_edge(self, source=None, target=None, weight=_SENTINEL, distance=_SENTINEL, cable=_SENTINEL):
        """Add an edge to the graph.

        Returns:
            None
        """
        if source is None or target is None:
            raise AttributeError("Invalid input!")
        if source not in self.vertices or target not in self.vertices:
            raise ValueError("Edge not exists")
        
        if weight is self._SENTINEL:
            # Lógica para lidar com o caso em que weight não foi fornecido
            weight = self.get_edge_weight(source, target)
        #else:
        #    print(f"Peso: {weight}")

        if distance is self._SENTINEL:
            # Lógica para lidar com o caso em que distance não foi fornecido
            distance = self.get_distance(source, target)
        #else:
        #    print(f"Distância: {distance}")

        if cable is self._SENTINEL:
            # Lógica para lidar com o caso em que cable não foi fornecido
            cable = self.get_cable(source, target)
        #else:
        #    print(f"Cabo: {cable}")

        edge = Edge(weight=weight, distance=distance, cable=cable)
        self.vertices[source].add_edge(self.vertices[target], edge)
        self.vertices[target].add_edge(self.vertices[source], edge)

    def set_vertex_weight(self, **kwargs):
        tag = kwargs.get('tag') if kwargs and 'tag' in kwargs else None
        weight = kwargs.get('weight') if kwargs and 'weight' in kwargs else None
        self.vertices[tag].update_vertex(weight=weight)

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

    def remove_vertex(self, source=None):
        """Remove a vertex and your edges from graph.

        Returns:
            None
        """
        if source is None:
            raise AttributeError("Invalid vertex!")
        
        tag_vertex_list = self.tag_adjacency_vertex_list(source)
        instance_source = self.vertices[source]
        for tag in tag_vertex_list:
            # self.vertices[tag].neighbors.pop(instance_source, None)
            del self.vertices[tag].neighbors[instance_source]   # Remove the entry with the old tag (more efficient than pop)
        #self.vertices.pop(source, None)
        del self.vertices[source]   # Remove the entry with the old tag (more efficient than pop)

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

        # self.vertices[source].neighbors.pop(self.vertices[target], None)
        # self.vertices[target].neighbors.pop(self.vertices[source], None)
        del self.vertices[source].neighbors[self.vertices[target]]  # Remove the entry with the old tag (more efficient than pop)
        del self.vertices[target].neighbors[self.vertices[source]]  # Remove the entry with the old tag (more efficient than pop)

    def BFS(self, start, array=None):
        """Performs a Breadth-First Search (BFS) on the graph.

        Args:
            start: The starting vertex (can be an integer or a string).
            array: An optional list to store the visited vertices. If None, a new list is created.

        Returns:
            list: A list of visited vertices in the order they were visited.
        
        Raises:
            ValueError: If the starting vertex is not found in the graph.
        """

        if array is None:
            array = []

        if start not in self.vertices:  # Check if the starting vertex exists
            raise ValueError(f"Starting vertex '{start}' not found in the graph.")

        visited = {vertex: False for vertex in self.vertices} # Use a dictionary for flexibility
        queue = deque([start])  # Use deque for efficiency and initialize with the start vertex
        visited[start] = True

        while queue:
            vertex = queue.popleft()  # Get the next vertex from the queue
            array.append(vertex)  # Append the visited vertex
            for neighbor in self.tag_adjacency_vertex_list(vertex):  # Iterate through the neighbors
                if not visited[neighbor]:
                    queue.append(neighbor)  # Add unvisited neighbors to the queue
                    visited[neighbor] = True  # Mark the neighbor as visited

        return array

    def DFS(self, start, visited=None, array=None):
        """Performs a Depth-First Search (DFS) on the graph.

        Args:
            start: The starting vertex (can be an integer or a string).
            visited: An optional set to keep track of visited vertices. If None, a new set is created.
            array: An optional list to store the visited vertices in order. If None, a new list is created.

        Raises:
            ValueError: If the starting vertex is not found in the graph.

        Returns:
            list: A list of visited vertices in the order they were visited.
        """

        if visited is None:
            visited = set()
        if array is None:
            array = []

        if start not in self.vertices:
            raise ValueError(f"Starting vertex '{start}' not found in the graph.")

        visited.add(start)
        array.append(start)  # Add the vertex to the array *before* the recursive calls

        for neighbor in self.tag_adjacency_vertex_list(start):
            if neighbor not in visited:
                self.DFS(neighbor, visited, array)  # Pass the array to recursive calls

        return array
    
    def rename_vertex(self, old=None, new=None):
        """Renames a vertex in the graph.

        Args:
            old: The current tag of the vertex.
            new: The new tag for the vertex.

        Raises:
            TypeError: If either vertex tag is not a string or an integer.
            ValueError: If either vertex tag is None or the old tag is not found.
        """

        if old is None or new is None:
            raise ValueError("Vertex tags cannot be None.")

        if not isinstance(old, (int, str)) or not isinstance(new, (int, str)):
            raise TypeError("Vertex tags must be integers or strings.")

        if old not in self.vertices:
            raise ValueError(f"Vertex with tag '{old}' not found.")
        
        if new in self.vertices:
            raise ValueError(f"Vertex with tag '{new}' already exist.")

        vertex = self.vertices[old]     # Get the vertex instance
        #vertex.set_tag(new)            # Update the vertex's tag
        vertex.tag = new                # Update the vertex's tag

        self.vertices[new] = vertex  # Add the vertex to the dictionary with the new tag
        # self.vertices.pop(old, None)
        del self.vertices[old]       # Remove the entry with the old tag (more efficient than pop)

    def update_vertex(self, tag=None, weight=None):
        if tag is None:
            raise ValueError("Tag cannot be None")
        if tag not in self.vertices:
            raise ValueError("Vertex not found")
        self.vertices[tag].update_vertex(weight=weight)

    def adjacency_list(self):
        """Renames a vertex in the graph.

        Args:
            None

        Returns:
            list: An adjacency list.
        """
        adj_list = {}
        for vertice in self.vertices.values():
            adj_list[vertice.tag] = vertice.get_neighbors_tag()
        return adj_list

    def __str__(self):
        grafo_str = ""
        for vertice in self.vertices.values():
            grafo_str += str(vertice) + "\n"
            for neighbor, edge in vertice.neighbors.items():
                grafo_str += f"  -> {neighbor}: {edge}\n"
        return grafo_str
