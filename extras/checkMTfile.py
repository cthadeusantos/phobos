import sqlite3

def check_sqlite_data(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Contar registros nas tabelas principais e auxiliares
    tables = ["main", "description", "voltage", "temperature", "manufacture", "conductor"]
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"Tabela {table}: {count} registros")

    # Verificar integridade das chaves estrangeiras
    cursor.execute("PRAGMA foreign_key_check;")
    fk_issues = cursor.fetchall()
    if fk_issues:
        print("\n⚠️ Problemas de integridade encontrados nas chaves estrangeiras:")
        for issue in fk_issues:
            print(issue)
    else:
        print("\n✅ Todas as chaves estrangeiras estão corretas.")

    # Exibir algumas amostras de dados inseridos
    print("\nAmostra de registros na tabela main:")
    cursor.execute("SELECT * FROM main LIMIT 5;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    conn.close()

# Executa a verificação
check_sqlite_data("mt.db")
