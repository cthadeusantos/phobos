import unittest
from source.electrical import ElectricalHandler

class TestElectrical(unittest.TestCase):

    def setUp(self):
        self.electrical = ElectricalHandler()

    def test_add_parameters(self):
        self.electrical.vline = 10
        self.electrical.vphase = 20
        self.assertEqual(self.electrical.vline, 10)
        self.assertEqual(self.electrical.vphase, 20)

    def test_invalid_parameters(self):
        with self.assertRaises(TypeError):
            self.electrical.vline = "10"