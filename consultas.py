import mysql.connector

CFG_BANCO = {
    "host": "localhost",
    "user": "root",
    "password": "1532",
    "database": "mon_clima"
}

def executar_consulta(cursor, titulo, sql): #funcao aux
    print(f"\n=== {titulo} ===")
    print(f"SQL: {sql.strip()}\n")
    cursor.execute(sql)
    resultados = cursor.fetchall()  # fetchall = busca todas as linhas

    for linha in resultados:
        print(" | ".join(str(v) for v in linha))

if __name__ == "__main__":
    conexao = mysql.connector.connect(**CFG_BANCO)
    cursor = conexao.cursor()

    executar_consulta(cursor, "Todos os registros",
        "SELECT id, cidade, temperatura, umidade, vento_kmh FROM registros_clima")

    executar_consulta(cursor, "Cidade mais quente",
        "SELECT cidade, temperatura FROM registros_clima ORDER BY temperatura DESC LIMIT 1")

    executar_consulta(cursor, "Cidade mais fria",
        "SELECT cidade, temperatura FROM registros_clima ORDER BY temperatura ASC LIMIT 1")

    executar_consulta(cursor, "Media de temperatura por cidade",
        "SELECT cidade, ROUND(AVG(temperatura),1) AS media FROM registros_clima GROUP BY cidade")

    executar_consulta(cursor, "Cidades com vento acima de 20 km/h",
        "SELECT cidade, vento_kmh FROM registros_clima WHERE vento_kmh > 20 ORDER BY vento_kmh DESC")

    executar_consulta(cursor, "Resumo geral",
        "SELECT COUNT(*) AS total, MIN(temperatura) AS minima, MAX(temperatura) AS maxima, ROUND(AVG(temperatura),1) AS media FROM registros_clima")

    cursor.close()
    conexao.close()