import unittest
from source.phobos import Phobos
from source.database import CableDBMT
from source.cable import Cable
from source.fileio import FileIO

class TestGraph(unittest.TestCase):
    def setUp(self):
        self.file = FileIO()
        self.cable_db = CableDBMT('databases/mt.db')
        self.phobos = Phobos()
     
if __name__ == '__main__':
    unittest.main()