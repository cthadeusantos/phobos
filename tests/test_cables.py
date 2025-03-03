import unittest
from source.cable import Cable
from source.database import CableDBMT

class TestCable(unittest.TestCase):

    # def test_tipo_setter(self):
    #     cable = Cable()
    #     cable.tipo = "Cobre"
    #     self.assertEqual(cable.tipo, "Cobre")
    #     #self.assertEqual(cable.resistanceCA, 0)
    #     #self.assertEqual(cable.reactance, 0)

    #     with self.assertRaises(TypeError):
    #         cable.tipo = 123  # Tentativa de atribuir um inteiro
    #         cable.tipo = Edge()
    #         #cable.resistanceCA = "A" 
    #         #cable.reactance = Edge() 

    def test_resistanceCC(self):
        cable = Cable()
        cable.resistanceCC = 10
        self.assertIsInstance(cable.resistanceCC, float)
        self.assertEqual(cable.resistanceCC, 10.0)
        
        cable.resistanceCC = 3.14159
        self.assertIsInstance(cable.resistanceCC, float)
        self.assertEqual(cable.resistanceCC, 3.14159)
        with self.assertRaises(TypeError):
            cable.resistanceCC = "abc"  # Tentativa de atribuir uma string não numérica
        with self.assertRaises(ValueError):
            cable.resistanceCC = -5  # Tentativa de atribuir um valor negativo

    def test_capacitance(self):
        cable = Cable(xc=2)
        cable.capacitance = 10
        self.assertIsInstance(cable.capacitance, float)
        self.assertEqual(cable.capacitance, 10.0)
        
        cable.capacitance = 3.14159
        self.assertIsInstance(cable.capacitance, float)
        self.assertEqual(cable.capacitance, 3.14159)
        with self.assertRaises(TypeError):
            cable.capacitance = "abc"  # Tentativa de atribuir uma string não numérica
        with self.assertRaises(ValueError):
            cable.capacitance = -5  # Tentativa de atribuir um valor negativo

    def test_resistanceCA(self):
        cable = Cable()
        cable.resistanceCA = 10
        self.assertIsInstance(cable.resistanceCA, float)
        self.assertEqual(cable.resistanceCA, 10.0)
        
        cable.resistanceCA = 3.14159
        self.assertIsInstance(cable.resistanceCA, float)
        self.assertEqual(cable.resistanceCA, 3.14159)
        with self.assertRaises(TypeError):
            cable.resistanceCA = "abc"  # Tentativa de atribuir uma string não numérica
        with self.assertRaises(ValueError):
            cable.resistanceCA = -5  # Tentativa de atribuir um valor negativo

    def test_reactance(self):
        cable = Cable(xl=5)
        self.assertIsInstance(cable.reactance, float)
        self.assertEqual(cable.reactance, 5.0)

        cable2 = Cable()
        with self.assertRaises(TypeError):
            cable2.reactance = "abc"  # Tentativa de atribuir uma string não numérica
        # with self.assertRaises(TypeError):
        #     a = Cable(10, 20)
        with self.assertRaises(ValueError):
            cable.reactance = -5  # Tentativa de atribuir um valor negativo

    def test_init_with_values(self):
        cabo = Cable(rca=25, xl=2)
        #self.assertEqual(cabo.tipo, "Alumínio")
        self.assertIsInstance(cabo.resistanceCA, float)
        self.assertEqual(cabo.resistanceCA, 25.0)
        self.assertIsInstance(cabo.reactance, float)
        self.assertEqual(cabo.reactance, 2.0)

    def test_impedance(self):
        cable = Cable(rca=25, xl=2)
        
        self.assertEqual(cable.impedance(), 25)
        self.assertEqual(cable.impedance(power_factor=0.7071067811865476), 19.091883092036785)

        with self.assertRaises(TypeError):
            cable.impedance(power_factor="A")
        with self.assertRaises(ValueError):
            cable.impedance(power_factor=1.009)
    
    def test_pf_angle_degree(self):
        cable = Cable(rca=25, xl=2)

        self.assertEqual(cable.pf_angle_degree(power_factor=0.7071067811865476), 45.0)
        self.assertEqual(cable.pf_angle_degree(), 0) 

        with self.assertRaises(TypeError):
            cable.pf_angle_degree(power_factor="A")
        with self.assertRaises(ValueError):
            cable.pf_angle_degree(power_factor=1.009)
    
    def test_parameters(self):
        db = CableDBMT('databases/mt.db')
        id, rcc, xc, rca, xl = db.get_data_from_db(id=212, installation=2)
        parameters = db.get_parameters_from_db(212)
        cable = Cable(rcc, xc, rca, xl, parameters)
        self.assertEqual(cable.get_parameter('voltage', 'id'), 3)
        self.assertEqual(cable.get_parameter('description', 'id'), 3)

    def test_read_db(self):
        db = CableDBMT('databases/mt.db')
        cable1 = Cable()
        cable2 = Cable()
        cable1.setting(db.get_cable_especifications(id=212, installation=2))
        cable2.setting(db.get_cable_especifications(id=165, installation=1))
        self.assertEqual(cable1.get_rcc(), 0.037)
        self.assertEqual(cable1.get_xc(), 5.15)
        self.assertEqual(cable1.get_rca(), 0.067)
        self.assertEqual(cable1.get_xl(), 0.24)
        self.assertEqual(cable2.get_rcc(), 0.387)
        self.assertEqual(cable2.get_xc(), 10.037)
        self.assertEqual(cable2.get_rca(), 0.506)
        self.assertEqual(cable2.get_xl(), 0.298)

if __name__ == '__main__':
    unittest.main()