import unittest
from source.cable import Cable
from source.edge import Edge

class TestCable(unittest.TestCase):

    def test_tipo_setter(self):
        cable = Cable()
        cable.tipo = "Cobre"
        self.assertEqual(cable.tipo, "Cobre")
        #self.assertEqual(cable.resistance, 0)
        #self.assertEqual(cable.reactance, 0)

        with self.assertRaises(TypeError):
            cable.tipo = 123  # Tentativa de atribuir um inteiro
            cable.tipo = Edge()
            #cable.resistance = "A" 
            #cable.reactance = Edge() 

    def test_resistance(self):
        cable = Cable()
        cable.resistance = 10
        self.assertIsInstance(cable.resistance, float)
        self.assertEqual(cable.resistance, 10.0)
        
        cable.resistance = 3.14159
        self.assertIsInstance(cable.resistance, float)
        self.assertEqual(cable.resistance, 3.14159)
        with self.assertRaises(TypeError):
            cable.resistance = "abc"  # Tentativa de atribuir uma string não numérica
        with self.assertRaises(ValueError):
            cable.resistance = -5  # Tentativa de atribuir um valor negativo

    def test_reactance(self):
        cable = Cable(reactance=5)
        self.assertIsInstance(cable.reactance, float)
        self.assertEqual(cable.reactance, 5.0)

        cable2 = Cable()
        with self.assertRaises(TypeError):
            cable2.reactance = "abc"  # Tentativa de atribuir uma string não numérica
        with self.assertRaises(TypeError):
            a = Cable(10, 20)
        with self.assertRaises(ValueError):
            cable.reactance = -5  # Tentativa de atribuir um valor negativo

    def test_init_with_values(self):
        cabo = Cable(tipo="Alumínio", resistance=25, reactance=2)
        self.assertEqual(cabo.tipo, "Alumínio")
        self.assertIsInstance(cabo.resistance, float)
        self.assertEqual(cabo.resistance, 25.0)
        self.assertIsInstance(cabo.reactance, float)
        self.assertEqual(cabo.reactance, 2.0)

if __name__ == '__main__':
    unittest.main()