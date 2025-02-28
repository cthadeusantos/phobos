import unittest
from source.fileio import FileIO

class TestSystem(unittest.TestCase):

    def setUp(self):
        self.instance = FileIO('data/test.json')

    def test_read(self):
        self.assertEqual(self.instance.read(), {
            "vpp": '100',
            "vpn": '50',
            "power_factor": '0.7',
            "root": "A"
            })

    def test_save(self):
        data = {
            "vpp": 100,
            "vpn": 50,
            "power_factor": 0.7,
            "root": "A"
            }
        self.instance.save(data, 'data/saida.json')
        self.assertTrue(self.instance.check_if_path_exists('data/saida.json'))
