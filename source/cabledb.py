import sqlite3
import os.path

class CablesDB:
    def __init__(self, db_name=None, rebuildDB=False):
        if db_name is None:
            raise AttributeError('Databae file not found. Please verify the file path.')
        self.database = db_name
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()
        if self.exists_file(self.database) and rebuildDB:
            self.criar_tabelas()

    def criar_tabelas(self):
        """Cria as tabelas normalizadas no banco de dados."""
        self.cursor.executescript(f"""
            CREATE TABLE IF NOT EXISTS installation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                value TEXT UNIQUE NOT NULL
            );

            CREATE TABLE IF NOT EXISTS temperature (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                value INTEGER UNIQUE NOT NULL
            );

            CREATE TABLE IF NOT EXISTS cablesection (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                value REAL UNIQUE NOT NULL
            );

            CREATE TABLE IF NOT EXISTS ratedvoltage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                value TEXT UNIQUE NOT NULL
            );


            CREATE TABLE IF NOT EXISTS material (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                value TEXT UNIQUE NOT NULL
            );

            CREATE TABLE IF NOT EXISTS cablesadakshdjkahdka (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                resistance REAL NOT NULL,
                reactance REAL NOT NULL,
                installation_id INTEGER NOT NULL,
                temperature_id INTEGER NOT NULL,
                cablesection_id INTEGER NOT NULL,
                ratedvoltage_id INTEGER NOT NULL,
                material_id INTEGER NOT NULL,
                FOREIGN KEY (id) REFERENCES installation(id),
                FOREIGN KEY (id) REFERENCES temperature(id),
                FOREIGN KEY (id) REFERENCES cablesection(id),
                FOREIGN KEY (id) REFERENCES ratedvoltage(id),
                FOREIGN KEY (id) REFERENCES material(id)
            );
        """)
        self.conn.commit()

    def inserir_valores_fixos(self):
        """Insere valores padrão nas tabelas auxiliares."""
        tabelas = {
            "installation": ["Em eletroduto", "Enterrado", "Aéreo"],
            "temperature": [60, 70, 75, 90],
            "cablesection": [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120],
            "ratedvoltage": ["0.6/1kV", "3.6/6kV", "6/10kV", "8.7/15kV", "12/20kV", "18/30kV"],
            "material": ["Cobre", "Alumínio"]
        }

        for tabela, valores in tabelas.items():
            for valor in valores:
                self.cursor.execute(f"INSERT OR IGNORE INTO {tabela} (value) VALUES (?)", (valor,))
        
        self.conn.commit()

    def obter_id(self, tabela, campo, valor):
        """Retorna o ID de um valor na tabela auxiliar ou insere caso não exista."""
        #campo = "valor" if tabela != "TipoInstalacao" else "descricao"
        self.cursor.execute(f"SELECT id FROM {tabela} WHERE {campo} = ?", (valor,))
        resultado = self.cursor.fetchone()

        if resultado:
            return resultado[0]
        else:
            self.cursor.execute(f"INSERT INTO {tabela} ({campo}) VALUES (?)", (valor,))
            self.conn.commit()
            return self.cursor.lastrowid

    def get_data(self, tabela='cables', campo='id', valor=0):
        """Retorna o ID de um valor na tabela auxiliar ou insere caso não exista."""
        #campo = "valor" if tabela != "TipoInstalacao" else "descricao"
        #self.cursor.execute(f"SELECT id, resistance, reactance, installation_id FROM {tabela} WHERE {campo} = ?", (valor,))
        #resultado = self.cursor.fetchone()

        """Consulta a tabela cables e recupera os valores das tabelas relacionadas."""
        self.cursor.execute(f"""SELECT 
                cables.id,
                cables.description,
                cables.resistance,
                cables.reactance,
                installation.value AS installation_value,
                temperature.value AS temperature_value,
                cablesection.value AS cablesection_value,
                ratedvoltage.value AS ratedvoltage_value,
                material.value AS material_value
            FROM cables
            JOIN installation ON cables.installation_id = installation.id
            JOIN temperature ON cables.temperature_id = temperature.id
            JOIN cablesection ON cables.cablesection_id = cablesection.id
            JOIN ratedvoltage ON cables.ratedvoltage_id = ratedvoltage.id
            JOIN material ON cables.material_id = material.id
            WHERE cables.id = ?""", (valor, ))
        #return self.cursor.fetchall()
        resultado = self.cursor.fetchone()

        if resultado:
            return resultado
        # else:
        #     self.cursor.execute(f"INSERT INTO {tabela} ({campo}) VALUES (?)", (valor,))
        #     self.conn.commit()
        #     return self.cursor.lastrowid
        return None

    def adicionar_cabo(self, description, resistance, reactance, installation_id, temperature_id, cablesection_id, ratedvoltage_id, material_id ):
        """Adiciona um cabo à tabela Cabos."""
        
        query = self.cursor.execute("""SELECT * FROM cables
                                    WHERE description = ? AND
                                    resistance = ? AND
                                    reactance = ? AND
                                    installation_id = ? AND
                                    temperature_id = ? AND
                                    cablesection_id = ? AND
                                    ratedvoltage_id = ? AND
                                    material_id = ?
                                    """,
                                    (description, resistance, reactance, installation_id, temperature_id, cablesection_id, ratedvoltage_id, material_id )
                                    ) # End of cursor
        exist = query.fetchone()
        if not exist:
            self.cursor.execute("""
                INSERT INTO cables (description, resistance, reactance, installation_id, temperature_id, cablesection_id, ratedvoltage_id, material_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (description,  resistance, reactance, installation_id, temperature_id, cablesection_id, ratedvoltage_id, material_id))
 
            self.conn.commit()

    def listar_cabos(self):
        """Lista os cabos junto com seus valores normalizados."""
        self.cursor.execute("""
            SELECT c.id, c.description, c.resistance, c.reactance,
                   ti.value, t.value, s.value, tn.value, mt.value
            FROM cables c
            JOIN installation ti ON c.id = ti.id
            JOIN temperature t ON c.id = t.id
            JOIN cablesection s ON c.id = s.id
            JOIN ratedvoltage tn ON c.id = tn.id
            JOIN material mt ON c.id = mt.id
        """)
        return self.cursor.fetchall()

    def fechar_conexao(self):
        self.conn.close()

    def exists_file(self, path_file):
        if os.path.exists(path_file):
            return True
        return False