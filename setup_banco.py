#Criado o banco de dados e as tabelas 
import mysql.connector

CFG_BANCO = {
    "host": "localhost",
    "user": "root",
    "password": "1532"
}

conexao = mysql.connector.connect(**CFG_BANCO)
cursor = conexao.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS mon_clima")
print("Banco criado!")
cursor.execute("USE mon_clima")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS registros_clima (
        id            INT AUTO_INCREMENT PRIMARY KEY,
        cidade        VARCHAR(100) NOT NULL,
        latitude      FLOAT NOT NULL,
        longitude     FLOAT NOT NULL,
        temperatura   FLOAT,
        umidade       INT,
        vento_kmh     FLOAT,
        consultado_em DATETIME DEFAULT NOW()
    )
""")
print("Tabela criada!")

cursor.close()
conexao.close()
print("Pronto! Rode agora: coletar_clima.py")
