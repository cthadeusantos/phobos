import random

from source.edge import Edge

# This class represents a vertex
# Parameters
# tag is a string or integer
# weight is a float
class Vertex:
    def __init__(self, tag=None, weight=0):
        self.tag = tag
        self.weight = weight
        self.neighbors = {}  # Dicionário para armazenar edges (vizinhos) e suas arestas

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, value):
        if value is None:
            value = str(hex(random.randint(1,16777215))).replace('0x','')
        self._tag = value

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        if not (isinstance(value, int) or isinstance(value, float)):
            raise TypeError("Weight needs to be a number")
        if value < 0:
            raise ValueError("Weight can be a non negative value.")
        self._weight = float(value)

    # def set_tag(self, value):
    #     self.tag = value

    # Get the vertex's tag
    def get_tag(self):
        return self.tag

    # Get the vertex's weight
    def get_weight(self):
        return self.weight
    
    # Add a new edge between self and target vertices
    def add_edge(self, target, edge):
        if not all(isinstance(obj, cls) for obj, cls in [(target, Vertex), (edge, Edge)]):
            raise TypeError("Invalid input!")
        self.neighbors[target] = edge
        target.neighbors[self] = edge

    # Return a list of neighbors' TAGs from vertex
    def get_neighbors_tag(self):
        return list(object.tag for object in list(self.neighbors.keys()))
    
    # Return a list of neighbors' Vertex instances from vertex
    def get_neighbors_objects(self):
        return list(object for object in list(self.neighbors.keys()))
    
    # return a specific edge instance between self and target
    def get_edge(self, target):
        return self.neighbors[target]

    # return a specific edge instance between self and target
    def get_num_edges(self, target):
        return len(self.neighbors)
    
    # return a list of edges instances from vertex
    def get_edges(self):
        return list(self.neighbors.values())

    # def update_vertex(self, **kwargs):
    #     tag = kwargs.get('tag') if kwargs and 'tag' in kwargs else None
    #     weight = kwargs.get('weight') if kwargs and 'weight' in kwargs else None
    #     if not isinstance(tag, (str, int)) or not isinstance(weight, (int, float)):
    #         raise TypeError("Invalid input!")
    #     if self.tag != tag:
    #         raise ValueError("Vertex invalid!")
    #     if tag is not None:
    #         self.tag = tag
    #     if weight is not None:
    #         self.weight = weight
    def update_vertex(self, tag=None, weight=None):
        """Update vertex parameters (tag or weight).

        Args:
            tag (str or int): New tag for the vertex. (optional)
            weight (int or float): New weight for the vertex. (optional)

        Returns:
            None
        """
        if tag is not None and not isinstance(tag, (str, int)):
            raise TypeError("Tag must be a string or an integer.")
        if weight is not None and not isinstance(weight, (int, float)):
            raise TypeError("Weight must be a number (int or float).")

        if tag is not None and self.tag != tag:
            raise ValueError("Vertex tag mismatch. Cannot update a different vertex.")

        self.tag = tag if tag is not None else self.tag # Mantém o valor atual se não for fornecido um novo
        self.weight = weight if weight is not None else self.weight # Mantém o valor atual se não for fornecido um novo

    def is_vertex_instance(self):
        if not isinstance(self.tag, Vertex):
            return False
        return True
    
    def is_vertex_str_or_int(self):
        if not isinstance(self.tag, (str, int)):
            return False
        return True

    def __str__(self):
        return f"Vertex: {self.tag} (Weight: {self.weight})"