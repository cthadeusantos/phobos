from math import sqrt

from source.graph import Graph
from source.vertex import Vertex
from source.electrical import ElectricalHandler

class System(Graph):

    class Sentinel(Graph.Sentinel):  # Herda de Graph.Sentinel
            pass

    def __init__(self, root=None, vpp=None, vpn=None, power_factor=None, data=None):
        """ Constructor

        Returns:
            None
        """
        super().__init__()
        if data is None:
            self.root = root
            self.power_factor = power_factor
            self.eletrical = ElectricalHandler(vpp, vpn)
            self.extra = {}
        else:
            self.root = data.get('root', None)
            self.vpp = data.get('vpp', None)
            self.vpn = data.get('vpn', None)
            self.power_factor = data.get('power_factor', None)

    class VertexExtraAttributes:
        def __init__(self, coordinates=(0,0), payload=0):
            self.coordinates = coordinates
            self.payload = payload

        @property
        def coordinates(self):
            return self._coordinates

        @coordinates.setter
        def coordinates(self, value=(0, 0)):
            if not isinstance(value, tuple) or len(value) != 2:  # Verifica se é tupla e tem 2 elementos
                raise TypeError("Coordinates must be a tuple of two numbers.")

            x, y = value  # Desempacota a tupla para facilitar o acesso

            if not isinstance(x, (int, float)):
                raise TypeError("X coordinate must be a number (int or float).")
            if not isinstance(y, (int, float)):
                raise TypeError("Y coordinate must be a number (int or float).")

            self._coordinates = (x, y) # Armazena como tupla

        @property
        def payload(self):
            """ load accumulated at the point """
            return self._payload

        @payload.setter
        def payload(self, value=0.0):
            # if value is None:
            #     raise ValueError("Payload value cannot be None")
            if value is not None:
                if not isinstance(value, (int, float)):
                    raise TypeError("Invalid payload value")

                if isinstance(value, (int, float)) and value < 0:
                    raise ValueError("Payload must be a non-negative integer.")
            self._payload = value

    @property
    def power_factor(self):
        return self._power_factor

    @power_factor.setter
    def power_factor(self, value=None):
        if value is not None:
            if not isinstance(value, (int, float)):
                raise TypeError("Invalid power factor value")

            if value <= 0 or value > 1:
                raise ValueError("Power factor must be between 0 and 1.")
        self._power_factor = value

    @property
    def vpp(self):
        return self._vpp

    @vpp.setter
    def vpp(self, value=None):
        if value is not None:
            if not isinstance(value, (int, float)):
                raise TypeError("Invalid power factor value")

            if value < 0:
                raise ValueError("Vpp must be between greater than 0")
        self._vpp = value

    @property
    def vpn(self):
        return self._vpn

    @vpn.setter
    def vpn(self, value=None):
        if value is not None:
            if not isinstance(value, (int, float)):
                raise TypeError("Invalid power factor value")

            if value < 0:
                raise ValueError("Vpn must be between greater than 0")
        self._vpn = value

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value=None):
        if value is not None:
            if not isinstance(value, (int, str)):
                raise TypeError("Invalid root value")

            if isinstance(value, int) and value < 0:
                raise ValueError("root must be a non-negative integer.")
        self._root = value

    def add_vertex(self, vertex=None, weight=0, coordinates=(0, 0), payload=0):
        super().add_vertex(vertex, weight)

        ########### WARNING
        ########### CHANGE HERE - AFTER
        ####### Create a new method to replace isinstance(tag, Vertex)
        if isinstance(vertex, Vertex):
            vertex = vertex.tag
        self.extra[vertex] = self.VertexExtraAttributes(coordinates=coordinates, payload=payload)

    def get_root(self):
        return self.root

    def check_vertex_is_valid(self, vertex):
        super().check_vertex_is_valid(vertex)
        if vertex not in self.extra:
            raise ValueError("Vertex not found")       

    def get_coordinates(self, vertex=None):
        self.check_vertex_is_valid(vertex)
        return self.extra[vertex].coordinates
    
    def get_payload(self, vertex=None):
        self.check_vertex_is_valid(vertex)
        return self.extra[vertex].payload

    def update_vertex(self, tag=None, **kwargs):
        self.check_vertex_is_valid(tag)
        coordinates = kwargs.get('coordinates') if kwargs and 'coordinates' in kwargs else None
        x1, y1 = coordinates if coordinates is not None else (0, 0)
        self.extra[tag].coordinates = (x1, y1)
        # self.extra[tag].coordinates_y = kwargs.get('coordinates_y') if kwargs and 'coordinates_y' in kwargs else None
        self.extra[tag].payload = kwargs.get('payload') if kwargs and 'payload' in kwargs else None
        weight = kwargs.get('weight') if kwargs and 'weight' in kwargs else None
        if weight is not None:
            super().update_vertex(tag, weight)

    ## FUNCAO PARA SER REFATORADA NO FUTURO
    ## FUI AJUSTANDO E FIQUEI DE SACO CHEIO PQ PRECISO FECHAR A funcao DFS_expert
    def add_edge(self, source=None, target=None, weight=0, distance=0, cable=None, coord_source=None, coord_target=None):
        if source in self.vertices and target in self.vertices:
            raise ValueError("Edge already exists")

        x1, y1 = coord_source if coord_source is not None else (0, 0)
        x2, y2 = coord_target if coord_target is not None else (0, 0)

        super().add_edge(source, target, weight, distance, cable=cable)

        if source not in self.extra and target not in self.extra:
            self.extra[source] = self.VertexExtraAttributes(coordinates=(x1, y1))
            self.extra[target] = self.VertexExtraAttributes(coordinates=(x2, y2))
        elif source not in self.extra:
            self.extra[source] = self.VertexExtraAttributes(coordinates=(x1, y1))
        elif target not in self.extra:
            self.extra[target] = self.VertexExtraAttributes(coordinates=(x2, y2))
        
        self.extra[source].coordinates = (x1, y1) if source is not None else (0, 0)
        self.extra[target].coordinates = (x2, y2) if target is not None else (0, 0)

    def update_edge(self, source=None, target=None, weight=Graph._SENTINEL, distance=Graph._SENTINEL, cable=Graph._SENTINEL, coord_source=Graph._SENTINEL, coord_target=Graph._SENTINEL):
        if source not in self.vertices or target not in self.vertices:
            raise ValueError("Edge not found")
        if coord_source is self._SENTINEL:
            # Lógica para lidar com o caso em que weight não foi fornecido
            coord_source = self.get_coordinates(source)
        else:
            if not (isinstance(coord_source, tuple) and len(coord_source) == 2):
                raise TypeError("Coordinates must be a tuple of two numbers.")

        if coord_target is self._SENTINEL:
            # Lógica para lidar com o caso em que weight não foi fornecido
            coord_target = self.get_coordinates(target)
        else:
            if not (isinstance(coord_target, tuple) and len(coord_target) == 2):
                raise TypeError("Coordinates must be a tuple of two numbers.")

        super().add_edge(source, target, weight, distance, cable=cable)

        self.extra[source] = self.VertexExtraAttributes(coordinates=coord_source)
        self.extra[target] = self.VertexExtraAttributes(coordinates=coord_target)

    #def DFS_expert(self, start=None, visited=None):
    def DFS_expert(self, start=None, visited=None):
        """Executa DFS e calcula a soma das cargas nos vértices e nas arestas."""

        if visited is None:
            visited = set()

        if start is None:
            raise ValueError(f"Root vertex '{start}' cannot be None.")

        if start not in self.vertices:
            raise ValueError(f"Root vertex '{start}' not found.")

        visited.add(start)

        # Inicializa a carga do vértice atual
        carga_ponto = self.get_carga_ponto(start)  # Método para obter a carga do vértice

        # Verifica se o vértice atual já possui carga calculada
        if self.extra[start].payload is None:
            self.extra[start].payload = carga_ponto

        for neighbor in self.tag_adjacency_vertex_list(start):
            if neighbor not in visited:
                self.DFS_expert(neighbor, visited)
                # Acumula a carga dos filhos no vértice pai
                value = self.extra[neighbor].payload
                if value is None:
                    value = 0
                if self.extra[start].payload is None:
                    self.extra[start].payload = 0
                self.extra[start].payload +=  self.extra[neighbor].payload # Atualiza a carga do vértice pai
                if not self.is_leaf(start):
                    self.extra[start].payload += self.get_edge_weight(start, neighbor)
        return self.extra
    
    def accumulate_payload(self, vertex=root):
        """Executa DFS_expert e retorna um dicionário com as cargas acumuladas."""
        if vertex is None:
            raise ValueError("Root vertex cannot be None.")
        cargas = self.DFS_expert(vertex)
        payload = {}
        for key, value in cargas.items():
            payload[key] = value.payload      
        return payload
    
    def get_carga_ponto(self, vertex):
        """Retorna a carga de um vértice."""
        return self.vertices[vertex].weight

    def reset(self):
        """Reset the instance of System"""
        return System()

    def get_data(self):
        for key, value in self.vertices:
            print(self.vertices[key], value)

    def __str__(self):
        return f"System: {self.root}"