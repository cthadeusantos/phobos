import unittest
from source.database import CableDBMT

class TestDB(unittest.TestCase):

    def setUp(self):
        self.db = CableDBMT(db_file='databases/mt.db')

    def test_openfile(self):

        with self.assertRaises(AttributeError):
            db = CableDBMT()  # Tentativa de abrir uma DB inválida
        self.assertEqual(self.db.get_id_from_db(185, 1, 2, 2, 1, 1), 84)
        self.assertEqual(self.db.get_data_from_db(84, 1), (84, 0.099, 4.213, 0.139, 0.249))
        self.assertEqual(self.db.get_data_from_db(250, 5), (250, 0.193, 13.111, 0.248, 0.142))

    def test_read_parameters(self):
        self.assertEqual(self.db.get_voltage_from_db(4), (4, '12/20kV'))
        self.assertEqual(self.db.get_manufacture_from_db(1), (1, 'Prysmian'))
        self.assertEqual(self.db.get_description_from_db(3), (3, 'Eprotenax'))
        self.assertEqual(self.db.get_conductor_from_db(1), (1, 'cooper'))
        self.assertEqual(self.db.get_temperature_from_db(1), (1, '105'))
    
    def test_read_parameters(self):
        self.assertEqual(self.db.get_parameters_from_db(212), {'gauge': 500.0, 'description': (3, 'Eprotenax'), 'voltage': (3, '8.7/15kV'), 'temperature': (2, '90'), 'manufacture': (1, 'Prysmian'), 'conductor': (1, 'cooper')})
        self.assertEqual(self.db.get_parameters_from_db(165), {'gauge': 50.0, 'description': (4, 'Voltalene'), 'voltage': (1, '3.6/6kV'), 'temperature': (2, '90'), 'manufacture': (1, 'Prysmian'), 'conductor': (1, 'cooper')})
        self.assertNotEqual(self.db.get_parameters_from_db(70), {'gauge': 50.0, 'description': (4, 'Voltalene'), 'voltage': (1, '3.6/6kV'), 'temperature': (2, '90'), 'manufacture': (1, 'Prysmian'), 'conductor': (1, 'cooper')})

    def test_get_data(self):
        self.assertEqual(self.db.get_data_from_db(id=212, installation=2), (212, 0.037, 5.15, 0.067, 0.24))
        self.assertEqual(self.db.get_data_from_db(id=165, installation=1), (165, 0.387, 10.037, 0.506, 0.298))

if __name__ == '__main__':
    unittest.main()