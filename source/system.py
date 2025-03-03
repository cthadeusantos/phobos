from math import sqrt, acos, sin, pi

from source.supergraph import Supergraph
from source.vertex import Vertex
from source.cable import Cable
from source.electrical import ElectricalHandler

class System(Supergraph):

    def __init__(self, root=None, vline=0, vphase=0, power_factor=0, data=None):
        """ Constructor

        Returns:
            None
        """
        super().__init__()
        if data is not None:
            self.root = data.get('root', None)
            self.vline = data.get('vline', 0)
            self.vphase = data.get('vphase', 0)
            self.vn = 0
            self.power_factor = data.get('power_factor', 0)
        else:
            self.root = root
            self.power_factor = power_factor
            self.vline = vline
            self.vphase = vphase
            self.vn = 0
        self.eletrical = ElectricalHandler(vline, vphase)
        self.extra = {}
        self.kfactor = {}
        self.total_segment = {}
        self.drop_voltage_segment = {}
        self.drop_voltage_accumulated = {}

    class Sentinel(Supergraph.Sentinel):  # Herda de Graph.Sentinel
        pass

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

    def set_vn(self, value):
        self.vn = value

    @property
    def power_factor(self):
        return self._power_factor

    @power_factor.setter
    def power_factor(self, value=None):
        if value is not None:
            if not isinstance(value, (int, float)):
                raise TypeError("Invalid power factor value")

            if value < 0 or value > 1:
                raise ValueError("Power factor must be between 0 and 1.")
        self._power_factor = value

    @property
    def vline(self):
        return self._vline

    @vline.setter
    def vline(self, value=None):
        if value is not None:
            if not isinstance(value, (int, float)):
                raise TypeError("Invalid power factor value")

            if value < 0:
                raise ValueError("vline must be between greater than 0")
        self._vline = value

    @property
    def vphase(self):
        return self._vphase

    @vphase.setter
    def vphase(self, value=None):
        if value is not None:
            if not isinstance(value, (int, float)):
                raise TypeError("Invalid power factor value")

            if value < 0:
                raise ValueError("vphase must be between greater than 0")
        self._vphase = value

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

    def get_setup(self):
        return {'vline': self.vline, 'vphase': self.vphase, 'power_factor': self.power_factor, 'root': self.root}

    def add_vertex(self, vertex=None, weight=0, coordinates=(0, 0), payload=0):
        super().add_vertex(vertex, weight)

        ########### WARNING
        ########### CHANGE HERE - AFTER
        ####### Create a new method to replace isinstance(tag, Vertex)
        if isinstance(vertex, Vertex):
            vertex = vertex.tag
        self.extra[vertex] = self.VertexExtraAttributes(coordinates=coordinates, payload=payload)

    def get_installation(self, source, target):
        target_instance = self.get_instance_vertex(target)
        return self.vertices[source].neighbors[target_instance].installation
    
    def set_installation(self, source, target, installation):
        target_instance = self.get_instance_vertex(target)
        self.vertices[source].neighbors[target_instance].installation=installation

    def serializeData(self):
        data = {
            "vline": self.vline,
            "vphase": self.vphase,
            "power_factor": self.power_factor,
            "root": self.root,
            }
        edges = {}
        rows = {}
        for source in self.vertices:
            if source not in rows:
                rows[source] = {}
            x, y = self.get_coordinates(source)
            rows[source]['vertex_weight'] = self.vertices[source].get_weight()
            rows[source]['coordinate_x'] = x
            rows[source]['coordinate_y'] = y
            edges[source]= {}
            for neighbor in self.vertices[source].neighbors:
                target = neighbor.tag
                weight = self.get_edge_weight(source, target)
                distance = self.get_distance(source, target)
                id = self.get_cable_id(source, target)
                installation = self.get_installation(source, target)
                edges[source][target] = {'edge_weight': weight, 'edge_distance': distance, 'cable_id': id, 'installation': installation}
            rows[source]['edges'] = edges[source]
        data['graph'] = rows
        return data

    def deserializeData(self, data=None, database=None):
        if data is None:
            raise AttributeError('Empty data!')
        graph = data.get('graph', {})
        if graph is {}:
            raise ImportError("Data are not formated!")
        self.root = data.get('root', None)
        self.vline = data.get('vline', 0)
        self.vphase = data.get('vphase', 0)
        self.power_factor = data.get('power_factor', 0)
        for source, value in graph.items():
            x = value.get('coordinate_x', 0.0)
            y = value.get('coordinate_y', 0.0)
            vweight = value.get('vertex_weight', 0.0)
            if len(edges := value.get('edges', {}).items()):
                for target, parameters in edges:
                    distance = parameters.get('edge_distance', 0.0)
                    eweight = parameters.get('edge_weight', 0.0)
                    cable_id = parameters.get('cable_id', 0.0)
                    cable = Cable()
                    installation = parameters.get('installation', 0)
                    cable.setting(database.get_cable_especifications(id=cable_id, installation=installation))
                    self.add_edge(source, target, eweight, distance, cable, installation, (x, y), overlap=True)
            else:
                self.add_vertex(source)
            self.set_vertex_weight(tag=source, weight=vweight)

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
    def add_edge(self, source=None, target=None, weight=0, distance=0, cable=None, installation=0, coord_source=None, coord_target=None, overlap=True, distributed=0):
        """
        coord_source: Coordinates x and y for source vertex (optional)
        coord_target: Coordinates x and y for target vertex (optional)
        skip: Jump if edge exists (optional)
        """    
        x1, y1 = coord_source if coord_source is not None else (0, 0)
        x2, y2 = coord_target if coord_target is not None else (0, 0)

        super().add_edge(source, target, weight, distance, cable=cable, overlap=overlap, distributed=distributed)

        if source not in self.extra and target not in self.extra:
            self.extra[source] = self.VertexExtraAttributes(coordinates=(x1, y1))
            self.extra[target] = self.VertexExtraAttributes(coordinates=(x2, y2))
        elif source not in self.extra:
            self.extra[source] = self.VertexExtraAttributes(coordinates=(x1, y1))
        elif target not in self.extra:
            self.extra[target] = self.VertexExtraAttributes(coordinates=(x2, y2))
        
        self.extra[source].coordinates = (x1, y1) if source is not None else (0, 0)
        self.extra[target].coordinates = (x2, y2) if target is not None else (0, 0)
        # target_instance = self.get_instance_vertex(target)
        # self.vertices[source].neighbors[target_instance].installation=installlation
        self.set_installation(source, target, installation)

    def update_edge(self, source=None, target=None, weight=Supergraph._SENTINEL, distance=Supergraph._SENTINEL, cable=Supergraph._SENTINEL, coord_source=Supergraph._SENTINEL, coord_target=Supergraph._SENTINEL, distributed=0):
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

        super().add_edge(source, target, weight, distance, cable=cable, distributed=distributed)

        self.extra[source] = self.VertexExtraAttributes(coordinates=coord_source)
        self.extra[target] = self.VertexExtraAttributes(coordinates=coord_target)

    def DFS_expert(self, start=None, visited=None):
        """Executa DFS e calcula a soma das cargas nos vértices e nas arestas."""

        if visited is None:
            visited = set()

        if start is None and self.root is None:
            raise ValueError(f"Root vertex '{start}' cannot be None.")
        
        if start is None and self.root is not None:
            start = self.root

        if start not in self.vertices:
            raise ValueError(f"Vertex '{start}' not found.")

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

                self._compute_segment_payload(start, neighbor)

                if not self.is_leaf(start):
                    self.extra[start].payload += self.get_edge_weight(start, neighbor)
        return self.extra
    
    def _compute_segment_payload(self, start=None, neighbor=None):
        if start is None or neighbor is None:
            raise ValueError(f"Vertex Cannot be None.")
        if self.get_distributed_type(start, neighbor) == 0 and self.get_edge_weight(start, neighbor) != 0:
            raise ValueError(f"The segment {start}-{neighbor} is not zero, so it must be a distributed payload or increase/decreasing payload.")
        if self.get_distributed_type(start, neighbor) == 1:
            value = self.get_edge_weight(start, neighbor) / 2
        elif self.get_distributed_type(start, neighbor) == 2:
            value = 2 * self.get_edge_weight(start, neighbor) / 3
        else:
            value = self.get_edge_weight(start, neighbor)
        if neighbor not in self.total_segment:
            self.total_segment[neighbor]={ start: self.extra[neighbor].payload }
        else:
            self.total_segment[neighbor][start] = self.extra[neighbor].payload

        self.total_segment[neighbor][start] += value

    def get_segment_payload_all(self):
        return self.total_segment

    def get_segment_payload(self, source=None, target=None):
        if source is None or target is None:
            raise ValueError(f'Invalid segment! source{source} target{target}')
        if target in self.total_segment:
            if source in self.total_segment[target]:
                return self.total_segment[target][source]
        if source in self.total_segment:
            if target in self.total_segment[source]:
                return self.total_segment[source][target]
        raise ValueError(f'Invalid segment! source{source} target{target}')
            

    def DFS_drop_voltage(self, start=None, visited=None, last=None):
        """Executa DFS e calcula a soma das cargas nos vértices e nas arestas."""

        if visited is None:
            visited = set()

        if start is None and self.root is None:
            raise ValueError(f"Root vertex '{start}' cannot be None.")
        
        if start is None and self.root is not None:
            start = self.root

        if start not in self.vertices:
            raise ValueError(f"Vertex '{start}' not found.")

        visited.add(start)

        if start == self.root:  # Inicializa a carga do vértice raiz e inicializa a tabela
            self.drop_voltage_accumulated[start] = self.get_drop_voltage_at_segment(start, '\u039F')  # Método para obter a carga do segmento
        else:
            if start not in self.drop_voltage_accumulated:
                self.drop_voltage_accumulated[start] = self.drop_voltage_accumulated[last]  # Inicializa vértice com queda de tensão do vértice pai
            self.drop_voltage_accumulated[start] += self.get_drop_voltage_at_segment(start, last) # Acumula queda de tensão

        for neighbor in self.tag_adjacency_vertex_list(start):
            if neighbor not in visited:
                self.DFS_drop_voltage(neighbor, visited, last=start)
    
    def get_drop_voltage_at_segment(self, source, target):
        if source in self.drop_voltage_segment:
            if target in self.drop_voltage_segment[source] or target == '\u039F':
                return self.drop_voltage_segment[source][target]
        if target in self.drop_voltage_segment:
            if source in self.drop_voltage_segment[target]:
                return self.drop_voltage_segment[target][source]
        raise ValueError(f"There is a invalid vertex. {source} or {target}")

    def accumulate_payload(self):
        """Executa DFS_expert e retorna um dicionário com as cargas acumuladas."""
        if self.root is None:
            raise ValueError("The vertex root cannot be None.")
        if self.root not in self.vertices:
            raise ValueError("You must have a root vertex to compute the drop voltage")
        self.DFS_expert()

    def payload_list(self):
        if not len(self.extra):
            raise ValueError("Extra vertex attributes cannot be empty!")
        payload = {}
        for key, value in self.extra.items():
            payload[key] = value.payload
        return payload

    def k_factor_table(self):
        self.kfactor = {}  # Inicializa kfactor como um dicionário vazio

        for source, value in self.vertices.items():
            for key1, value in self.vertices[source].neighbors.items():
                target = key1.get_tag()
                cable = self.get_cable(source, target)
                rca = cable.get_rca()
                xl = cable.get_xl()
                k = self.calc_kfactor(rca, xl)

                if (source in self.kfactor and target in self.kfactor[source]) or \
                (target in self.kfactor and source in self.kfactor[target]):
                    continue

                if source not in self.kfactor:
                    self.kfactor[source] = {}  # Inicializa o dicionário interno para o vértice

                self.kfactor[source][target] = k  # Adiciona o kfactor para o vértice e o vizinho

    def get_kfactor(self, source, target):
        if source in self.kfactor:
            if target in self.kfactor[source]:
                return self.kfactor[source][target]
        if target in self.kfactor:
            if source in self.kfactor[target]:
                return self.kfactor[target][source]
        raise ValueError(f"There is a invalid vertex. {source} or {target}")

    def calc_kfactor(self, r, x):
        """
        Compute k-factor.

        Args:
            r (float): Valor de r.
            x (float): Valor de x.

        Returns:
            float: O valor do kfactor.
        """
        if self.vn == 0:
            raise ZeroDivisionError("vline cannot be zero.")

        angle = self.angle_pf_radix()
        pf = self.power_factor
        vn_squared = self.vn ** 2

        numerator = (r * pf) + (x * sin(angle))
        result = (numerator / vn_squared) * 100

        return result

    def compute_drop_voltage_segment(self):
        """
        Compute the percent drop voltage for the stretch
        """
        self.drop_voltage_segment = {self.root: {'\u039F': 0.0 }}  # Start drop voltage dictionary (point - zero)
        
        if not len(self.kfactor):
            self.k_factor_table()

        for source, value in self.vertices.items():
            for key1, value in self.vertices[source].neighbors.items():
                target = key1.get_tag()
                #stretch_dv = self.get_kfactor(source, target) * self.get_payload(target) * self.get_distance(source, target)
                stretch_dv = self.get_kfactor(source, target) * self.get_segment_payload(target, source) * self.get_distance(source, target)
                if (source in self.drop_voltage_segment and target in self.drop_voltage_segment[source]) or \
                (target in self.drop_voltage_segment and source in self.drop_voltage_segment[target]):
                    continue
                if source not in self.drop_voltage_segment:
                    self.drop_voltage_segment[source] = {}
                if target not in self.drop_voltage_segment[source]:
                    self.drop_voltage_segment[source][target] = 0.0
                self.drop_voltage_segment[source][target] = stretch_dv

    # def set_total_segment(self):
    #     """
    #     Compute the percent drop voltage for the stretch
    #     """
    #     self.drop_voltage_segment = {self.root: {'\u039F': 0.0 }}  # Start drop voltage dictionary (point - zero)
        
    #     if not len(self.kfactor):
    #         self.k_factor_table()

    #     for source, value in self.vertices.items():
    #         for key1, value in self.vertices[source].neighbors.items():
    #             target = key1.get_tag()
    #             stretch_dv = self.get_kfactor(source, target) * self.get_payload(target) * self.get_distance(source, target)
    #             if (source in self.drop_voltage_segment and target in self.drop_voltage_segment[source]) or \
    #             (target in self.drop_voltage_segment and source in self.drop_voltage_segment[target]):
    #                 continue
    #             if source not in self.drop_voltage_segment:
    #                 self.drop_voltage_segment[source] = {}
    #             if target not in self.drop_voltage_segment[source]:
    #                 self.drop_voltage_segment[source][target] = 0.0
    #             self.drop_voltage_segment[source][target] = stretch_dv

    def drop_voltage_segment_list(self):
        return self.drop_voltage_segment

    def get_vertex_tag_from_instance(self, instance):
        if instance in self.reverse_vertices:
            return self.reverse_vertices[instance].get_tag()
        raise ValueError("Vertex instance not found!")

    def angle_pf_radix(self):
        """
        Return angle of power factor in radix
        """
        return acos(self.power_factor) # Angle in radix

    def angle_pf_degree(self):
        """
        Return angle of power factor in degree
        """
        return (acos(self.power_factor) * 180) / pi # Angle in degree

    def get_carga_ponto(self, vertex):
        """Retorna a carga de um vértice."""
        return self.vertices[vertex].weight

    def reset(self):
        """Reset the instance of System"""
        return System()

    def get_data(self):
        """
        Funcao ainda nao faz nada
        """
        for key, value in self.vertices:
            print(self.vertices[key], value)

    def compute_system(self):
        self.accumulate_payload()
        self.k_factor_table()
        self.compute_drop_voltage_segment()
        self.DFS_drop_voltage()

    def __str__(self):
        return f"System: {self.root}"