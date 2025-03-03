import pandas as pd
import sqlite3
import os

def process_excel_to_sqlite(file_path, sheet_name, db_path):
    # Ler a planilha
    df = pd.read_excel(file_path, sheet_name=sheet_name, decimal=',')
    
    # Converter colunas de A a N para float e arredondar para 3 casas decimais
    cols_to_round = df.columns[8:22]  # A até N (supondo que começam na coluna 8)

    #df[cols_to_round] = df[cols_to_round].apply(lambda x: x.str.replace(',', '.').astype(float).round(3))
    df[cols_to_round] = df[cols_to_round].round(3)

    
    # Criar conexão com SQLite
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Criar tabelas auxiliares
    for col in ['description', 'voltage', 'temperature', 'manufacture', 'conductor']:
        cursor.execute(f"""
            CREATE TABLE {col} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
        """)
    
    # Criar tabela principal
    cursor.execute("""
        CREATE TABLE main (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gauge REAL,
            description_id INTEGER,
            voltage_id INTEGER,
            min REAL,
            max REAL,
            temperature_id INTEGER,
            manufacture_id INTEGER,
            conductor_id INTEGER,
            A REAL, B REAL, C REAL, D REAL, E REAL, F REAL, G REAL, H REAL, I REAL, J REAL, K REAL, L REAL, M REAL, N REAL,
            FOREIGN KEY(description_id) REFERENCES description(id),
            FOREIGN KEY(voltage_id) REFERENCES voltage(id),
            FOREIGN KEY(temperature_id) REFERENCES temperature(id),
            FOREIGN KEY(manufacture_id) REFERENCES manufacture(id),
            FOREIGN KEY(conductor_id) REFERENCES conductor(id)
        )
    """)
    
    # Inserir dados nas tabelas auxiliares e obter IDs
    def get_or_create(table, value):
        cursor.execute(f"SELECT id FROM {table} WHERE name = ?", (value,))
        row = cursor.fetchone()
        if row:
            return row[0]
        cursor.execute(f"INSERT INTO {table} (name) VALUES (?)", (value,))
        return cursor.lastrowid
    
    # Inserir dados na tabela principal
    for _, row in df.iterrows():
        desc_id = get_or_create('description', row['description'])
        volt_id = get_or_create('voltage', row['voltage'])
        temp_id = get_or_create('temperature', row['temperature'])
        manuf_id = get_or_create('manufacture', row['manufacture'])
        condu_id = get_or_create('conductor', row['conductor'])
        
        cursor.execute("""
            INSERT INTO main (gauge, description_id, voltage_id, min, max, temperature_id, manufacture_id, conductor_id,
                                        A, B, C, D, E, F, G, H, I, J, K, L, M, N)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (row['gauge'], desc_id, volt_id, row['min'], row['max'], temp_id, manuf_id, condu_id) + tuple(row[cols_to_round]))
    
    conn.commit()
    conn.close()

# Executar a função com os arquivos e caminhos desejados
process_excel_to_sqlite('sheets/medium_voltage.xlsx', 'attributes01', 'mt.db')
