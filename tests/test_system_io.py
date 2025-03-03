import unittest

from source.system import System
from source.vertex import Vertex
from source.database import CableDBMT
from source.cable import Cable
from source.fileio import FileIO

class TestSystem(unittest.TestCase):

    def setUp(self):
        self.system = System()
        self.file = FileIO()
        self.cable_db = CableDBMT('databases/mt.db')

    def test_save_file(self):
        data = { 'root': '1', 'vline': 220, 'vphase': 127, 'power_factor': 0.5 }
        
        phobos = System(data=data)

        phobos.add_vertex('A', 10)
        phobos.add_vertex('B', 11)
        phobos.add_vertex('C', 12)
        phobos.add_vertex('D', 14)
        phobos.add_vertex('E', 15)
        phobos.add_vertex('F', 16)
        phobos.add_vertex('G', 17)
        phobos.add_vertex('H', 18)
        phobos.add_vertex('I', 19)

        phobos.add_edge("A", "B")

        cable1 = Cable()
        cable1.setting(self.cable_db.get_cable_especifications(id=180, installation=2))
        cable2 = Cable()
        cable2.setting(self.cable_db.get_cable_especifications(id=150, installation=1))
        cable3 = Cable()
        cable3.setting(self.cable_db.get_cable_especifications(id=88, installation=0))

        phobos.update_edge('A','C', 21, 100, cable=cable1)
        phobos.update_edge('A','B', 22, 101, cable=cable1)
        phobos.update_edge('B','D', 23, 102, cable=cable2)
        phobos.update_edge('B','E', 24, 103, cable=cable2)
        phobos.update_edge('E','I', 25, 104, cable=cable1)
        phobos.update_edge('C','F', 26, 105, cable=cable3)
        phobos.update_edge('C','H', 26, 106, cable=cable3)
        phobos.update_edge('G','F', 28, 107, cable=cable3)

        data = phobos.serializeData()

        self.file.save(data, 'data/test.json')

        with open('data/test.json') as file:
            textfile = file.read()

        self.assertEqual(textfile, """{
    "graph": {
        "A": {
            "coordinate_x": 0,
            "coordinate_y": 0,
            "edges": {
                "B": {
                    "cable_id": 180,
                    "edge_distance": 101.0,
                    "edge_weight": 22.0,
                    "installation": null
                },
                "C": {
                    "cable_id": 180,
                    "edge_distance": 100.0,
                    "edge_weight": 21.0,
                    "installation": null
                }
            },
            "vertex_weight": 10.0
        },
        "B": {
            "coordinate_x": 0,
            "coordinate_y": 0,
            "edges": {
                "A": {
                    "cable_id": 180,
                    "edge_distance": 101.0,
                    "edge_weight": 22.0,
                    "installation": null
                },
                "D": {
                    "cable_id": 150,
                    "edge_distance": 102.0,
                    "edge_weight": 23.0,
                    "installation": null
                },
                "E": {
                    "cable_id": 150,
                    "edge_distance": 103.0,
                    "edge_weight": 24.0,
                    "installation": null
                }
            },
            "vertex_weight": 11.0
        },
        "C": {
            "coordinate_x": 0,
            "coordinate_y": 0,
            "edges": {
                "A": {
                    "cable_id": 180,
                    "edge_distance": 100.0,
                    "edge_weight": 21.0,
                    "installation": null
                },
                "F": {
                    "cable_id": 88,
                    "edge_distance": 105.0,
                    "edge_weight": 26.0,
                    "installation": null
                },
                "H": {
                    "cable_id": 88,
                    "edge_distance": 106.0,
                    "edge_weight": 26.0,
                    "installation": null
                }
            },
            "vertex_weight": 12.0
        },
        "D": {
            "coordinate_x": 0,
            "coordinate_y": 0,
            "edges": {
                "B": {
                    "cable_id": 150,
                    "edge_distance": 102.0,
                    "edge_weight": 23.0,
                    "installation": null
                }
            },
            "vertex_weight": 14.0
        },
        "E": {
            "coordinate_x": 0,
            "coordinate_y": 0,
            "edges": {
                "B": {
                    "cable_id": 150,
                    "edge_distance": 103.0,
                    "edge_weight": 24.0,
                    "installation": null
                },
                "I": {
                    "cable_id": 180,
                    "edge_distance": 104.0,
                    "edge_weight": 25.0,
                    "installation": null
                }
            },
            "vertex_weight": 15.0
        },
        "F": {
            "coordinate_x": 0,
            "coordinate_y": 0,
            "edges": {
                "C": {
                    "cable_id": 88,
                    "edge_distance": 105.0,
                    "edge_weight": 26.0,
                    "installation": null
                },
                "G": {
                    "cable_id": 88,
                    "edge_distance": 107.0,
                    "edge_weight": 28.0,
                    "installation": null
                }
            },
            "vertex_weight": 16.0
        },
        "G": {
            "coordinate_x": 0,
            "coordinate_y": 0,
            "edges": {
                "F": {
                    "cable_id": 88,
                    "edge_distance": 107.0,
                    "edge_weight": 28.0,
                    "installation": null
                }
            },
            "vertex_weight": 17.0
        },
        "H": {
            "coordinate_x": 0,
            "coordinate_y": 0,
            "edges": {
                "C": {
                    "cable_id": 88,
                    "edge_distance": 106.0,
                    "edge_weight": 26.0,
                    "installation": null
                }
            },
            "vertex_weight": 18.0
        },
        "I": {
            "coordinate_x": 0,
            "coordinate_y": 0,
            "edges": {
                "E": {
                    "cable_id": 180,
                    "edge_distance": 104.0,
                    "edge_weight": 25.0,
                    "installation": null
                }
            },
            "vertex_weight": 19.0
        }
    },
    "power_factor": 0.5,
    "root": "1",
    "vline": 220,
    "vphase": 127
}""")

    def test_read_file(self):
        data = { 'root': '1', 'vline': 220, 'vphase': 127, 'power_factor': 0.5 }
        phobos = System(data=data)
        data = self.file.read('data/entrada.json')
        cable_db = CableDBMT('databases/mt.db')
        phobos.deserializeData(data, database=cable_db)
        self.assertEqual(phobos.get_neighbors('C'), ['A', 'F', 'H'])
        self.assertEqual(phobos.get_edge_weight('I', 'E'), 25.0)

        x =  phobos.get_cable('A', 'C')

        self.assertEqual(phobos.get_cable('A','C').get_rcc(), 0.193)
        self.assertEqual(phobos.get_cable('A','C').get_xc(), 7.702)
        self.assertEqual(phobos.get_cable('A','C').get_rca(), 0.251)
        self.assertEqual(phobos.get_cable('A','C').get_xl(), 0.201)

        self.assertEqual(phobos.get_cable('B','D').get_rcc(), 0.727)
        self.assertEqual(phobos.get_cable('B','D').get_xc(), 10.739)
        self.assertEqual(phobos.get_cable('B','D').get_rca(), 0.933)
        self.assertEqual(phobos.get_cable('B','D').get_xl(), 0.228)

        self.assertEqual(phobos.get_cable('C','F').get_rcc(), 0.037)
        self.assertEqual(phobos.get_cable('C','F').get_xc(), 3.062)
        self.assertEqual(phobos.get_cable('C','F').get_rca(), 0.055)
        self.assertEqual(phobos.get_cable('C','F').get_xl(), 0.055)

        with self.assertRaises(ValueError):
            self.assertEqual(phobos.get_cable('Z','F').get_xl(), 0.055)
            self.assertEqual(phobos.get_cable('C','Z').get_xl(), 0.055)

if __name__ == '__main__':
    unittest.main()