from collections import defaultdict
from queue import Queue
from collections import deque 

from source.graph import Graph
from source.superedge import Superedge

class Supergraph(Graph):

    class Sentinel:
            pass

    _SENTINEL = Sentinel()

    def __init__(self):
        """ Constructor

        Returns:
            None
        """
        super().__init__()

    def get_cable_id(self, source=None, target=None):
        return self.get_cable(source, target).id              
    
    def get_cable(self, source=None, target=None):
        if source is None or target is None:
            raise ValueError("Vertex cannot be None")
        if source not in self.vertices or target not in self.vertices:
            raise ValueError("Vertex not found")
        if not isinstance(source, (str, int)) and not isinstance(target, (str, int)):
            raise TypeError("Invalid input!")
        instance = self.vertices[target]
        return self.vertices[source].neighbors[instance].cable

    def get_distributed_type(self, source=None, target=None):
        if source is None or target is None:
            raise ValueError("Vertex cannot be None")
        if source not in self.vertices or target not in self.vertices:
            raise ValueError("Vertex not found")
        if not isinstance(source, (str, int)) and not isinstance(target, (str, int)):
            raise TypeError("Invalid input!")
        instance = self.vertices[target]
        return self.vertices[source].neighbors[instance].distributed_type

    def add_edge(self, source=None, target=None, weight=0, distance=0, cable=None, overlap=True, distributed=0):
        """Add an edge to the graph.

        Returns:
            None
        """
        if source is None or target is None:
            raise AttributeError("Invalid input!")
        edge = Superedge(weight, distance, cable=cable, distributed=distributed)
        super().add_edge_aux(source, target, overlap, edge)

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

        edge = Superedge(weight=weight, distance=distance, cable=cable)
        self.vertices[source].add_edge(self.vertices[target], edge)
        self.vertices[target].add_edge(self.vertices[source], edge)
            
