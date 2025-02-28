import unittest
import sqlite3

from source.cabledb import CablesDB

class TestCableDB(unittest.TestCase):   

    def test_criar_tabelas(self):
        with self.assertRaises(AttributeError):
            db = CablesDB()
        db = CablesDB(db_name='testtable', rebuildDB=True)
        db.inserir_valores_fixos()

    def test_listar_cabos(self):
        db = CablesDB(db_name='testtable')
        db.inserir_valores_fixos()
        #"""cursor = sqlite3.connect("cables.db")"""
        inst_id = db.obter_id('installation', 'value', 'Enterrado')
        temp_id = db.obter_id("temperature", 'value', '60')
        sect_id = db.obter_id("cablesection", "value", 1.5)
        volt_id = db.obter_id("ratedvoltage", "value", '3.6/6kV')
        mate_id = db.obter_id("material", "value",'Cobre')

        db.adicionar_cabo("Cabo 1 especial", 10, 10, inst_id, temp_id, sect_id, volt_id, mate_id)
        temp_id = db.obter_id("temperature", 'value', '90')
        volt_id = db.obter_id("ratedvoltage", "value", '6/10kV')
        db.adicionar_cabo("Cabo 2 especial", 20, 20, inst_id, temp_id, sect_id, volt_id, mate_id)
        
        self.assertEqual(db.listar_cabos(), [(1, 'Cabo 1 especial', 10.0, 10.0, 'Em eletroduto', 60, 1.5, '0.6/1kV', 'Cobre'),
                                             (2, 'Cabo 2 especial', 20.0, 20.0, 'Enterrado', 70, 2.5, '3.6/6kV', 'Alumínio')])
    
    def test_get_data_cable(self):
        db = CablesDB(db_name='testtable')
        self.assertEqual(db.get_data("cables", "id", 1), (1, 'Cabo 1 especial', 10.0, 10.0, 'Enterrado', 60, 1.5, '3.6/6kV', 'Cobre'))

if __name__ == '__main__':
    unittest.main()