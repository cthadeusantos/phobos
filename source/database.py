from abc import ABC, abstractmethod
import sqlite3

class cableDB(ABC):
    
    # def __init__(self, db_file=None):
    #     if db_file is None:
    #         raise AttributeError('Invalid database filename')
    #     self.db_path = db_file

    @staticmethod
    def get_id_from_db(self):
        pass

    @staticmethod    
    def get_id_name_from_db(self):
        pass

    @staticmethod
    def get_voltage_from_db(self):
        pass

    @staticmethod
    def get_description_from_db(self):
        pass

    @staticmethod
    def get_manufacture_from_db(self):
        pass

    @staticmethod    
    def get_conductor_from_db(self):
        pass

    @staticmethod
    def get_temperature_from_db(self):
        pass

    @staticmethod
    def get_data_from_db(self):
        pass
    
    @staticmethod
    def get_parameters_from_db(self):
        pass

class CableDBMT(cableDB):
    def __init__(self, db_file=None):
        if db_file is None:
            raise AttributeError('Invalid database filename')
        self.db_path = db_file
    
    def get_id_from_db(self, gauge, voltage_id, description_id, temperature_id, manufacture_id, conductor_id, table_name='main'):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Consulta SQL para buscar os valores correspondentes
        query = f"""
            SELECT id
            FROM {table_name}
            WHERE voltage_id = ? AND description_id = ? 
                  AND temperature_id = ? AND manufacture_id = ?
                  AND conductor_id = ? AND gauge = ?
        """

        cursor.execute(query, (voltage_id, description_id, temperature_id, manufacture_id, conductor_id, gauge))
        result = cursor.fetchone()

        conn.close()

        if not result:
            return None  # Retorna None se não encontrar dados correspondentes

        # Atribuir valor
        id = result[0]   # id

        return id
    
    def seek_parameters_from_db(self, id=id, table_name='main'):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Consulta SQL para buscar os valores correspondentes
        query = f"""
            SELECT gauge, voltage_id, description_id, temperature_id, manufacture_id, conductor_id, gauge
            FROM {table_name}
            WHERE id = ?
        """

        cursor.execute(query, (id,))
        result = cursor.fetchone()

        conn.close()

        if not result:
            return None  # Retorna None se não encontrar dados correspondentes

        # Atribuir valor
        gauge = result[0]
        voltage_id = result[1]   # id
        description_id = result[2]   # id
        temperature_id = result[3]   # id
        manufacture_id = result[4]   # id
        conductor_id = result[5]   # id

        return gauge, voltage_id, description_id, temperature_id, manufacture_id, conductor_id

    def get_id_name_from_db(self, table_name,  id_value, id_column='id'):
        """
        Função genérica para obter id e name de uma tabela.

        Args:
            table_name (str): Nome da tabela.
            id_column (str): Nome da coluna de ID.
            id_value: Valor do ID a ser buscado.

        Returns:
            tuple: (id, name) se encontrado, None caso contrário.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            query = f"""
                SELECT id, name
                FROM {table_name}
                WHERE {id_column} = ?
            """

            cursor.execute(query, (id_value,))
            result = cursor.fetchone()

            conn.close()

            if not result:
                return None

            id, name = result[0], result[1]
            return (id, name)

        except sqlite3.Error as e:
            print(f"Erro ao buscar dados: {e}")
            return None

    def get_voltage_from_db(self, voltage_id):
        """
        Return: A tuple
        """
        return self.get_id_name_from_db("voltage", voltage_id)

    def get_description_from_db(self, description_id):
        """
        Return: A tuple
        """
        return self.get_id_name_from_db("description", description_id)

    def get_manufacture_from_db(self, manufacture_id):
        """
        Return: A tuple
        """
        return self.get_id_name_from_db("manufacture", manufacture_id)

    def get_conductor_from_db(self, conductor_id):
        """
        Return: A tuple
        """
        return self.get_id_name_from_db("conductor", conductor_id)

    def get_temperature_from_db(self, temperature_id):
        """
        Return: A tuple
        """
        return self.get_id_name_from_db("temperature", temperature_id)
    
    def get_data_from_db(self, id, installation, table_name='main'):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Consulta SQL para buscar os valores correspondentes
        query = f"""
            SELECT A, B, C, D, E, F, G, H, I, J, K, L, M, N, id
            FROM {table_name}
            WHERE id = ?
        """

        cursor.execute(query, (id,))
        result = cursor.fetchone()

        conn.close()

        if not result:
            return None  # Retorna None se não encontrar dados correspondentes

        # Distribuir valores na tupla (W, X, Y, Z)
        W, X = result[0], result[1]  # A -> W, B -> X

        # Determinar índices de Y e Z com base no parâmetro installation
        install_index = 2 + (installation * 2)
        if install_index >= len(result):  
            return None  # Retorna None se installation for inválido

        Y, Z = result[install_index], result[install_index + 1]

        cable_id = result[14]

        return (cable_id, W, X, Y, Z)
    
    def get_parameters_from_db(self, id, table_name='main'):
        gauge, voltage_id, description_id, temperature_id, manufacture_id, conductor_id = self.seek_parameters_from_db(id, table_name)
        a = self.get_conductor_from_db(conductor_id)
        b = self.get_description_from_db(description_id)
        c = self.get_manufacture_from_db(manufacture_id)
        d = self.get_temperature_from_db(temperature_id)
        e = self.get_voltage_from_db(voltage_id)

        return {
            'gauge': gauge,
            'conductor': a,
            'description': b,
            'manufacture': c,
            'temperature': d,
            'voltage': e,
            }
    
    def get_cable_especifications(self, id=1, installation=0):
        """
        Get cable data
        """
        data = self.get_data_from_db(id=id, installation=installation)
        parameters = self.get_parameters_from_db(id=id)
        return data, parameters
    
    def set_cable_especifications(self, id=1, installation=0):
        """
        Rearranges parameters to suit Cable Class parameters
        """
        data, parameters = self.get_cable_especifications(id, installation)
        return data[1], data[2], data[3], data[4], parameters, data[0]

class CableDBBT(cableDB):
    pass