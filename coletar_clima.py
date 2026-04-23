import requests ## requests = biblioteca para fazer chamadas a APIs (buscar dados da internet)
import mysql.connector


CFG_BANCO = {
    "host": "localhost",
    "user": "root",
    "password": "1532",
    "database": "mon_clima"
}

# Lista de cidades que vamos consultar
# Cada cidade é um dicionário com nome, latitude e longitude
# Latitude e longitude são as coordenadas geográficas da cidade
CIDADES = [
    {"nome": "Caxias do Sul",  "latitude": -29.168, "longitude": -51.179},
    {"nome": "Farroupilha",    "latitude": -29.224, "longitude": -51.345},
    {"nome": "Porto Alegre",   "latitude": -30.033, "longitude": -51.230},
    {"nome": "São Paulo",      "latitude": -23.550, "longitude": -46.633},
    {"nome": "Rio de Janeiro", "latitude": -22.906, "longitude": -43.172},
]

def buscar_clima(latitude, longitude):

    #API ME ENDERECO
    url = "https://api.open-meteo.com/v1/forecast"

    # Parâmetros que enviamos junto com a chamada
    # É como preencher um formulário antes de mandar
    parametros = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "wind_speed_unit": "kmh"
    }
    try: 
        resposta = requests.get(url, params=parametros, timeout=10)
        # Verifica se deu certo (código 200 = sucesso)
        resposta.raise_for_status()

        # Converte o resultado de JSON para dicionário Python
        dados = resposta.json()

        # Acessa a parte "current" dentro do dicionário retornado
        atual = dados["current"]

        return {
            "temperatura": atual["temperature_2m"],
            "umidade":     atual["relative_humidity_2m"],
            "vento_kmh":   atual["wind_speed_10m"]
        }
    except requests.exceptions.RequestException as erro:
        print(f"Erro na API: {erro}")
        return None
    
    # Recebe o cursor, a cidade e os dados de clima
def salvar_no_banco(cursor, cidade, dados):
    sql = """
        INSERT INTO registros_clima
            (cidade, latitude, longitude, temperatura, umidade, vento_kmh)
        VALUES
            (%s, %s, %s, %s, %s, %s)
    """
    valores = ( #tupla com os mesmos valeres e ordem 
        cidade["nome"],
        cidade["latitude"],
        cidade["longitude"],
        dados["temperatura"],
        dados["umidade"],
        dados["vento_kmh"]
    )
    cursor.execute(sql, valores)

if __name__ == "__main__":# Bloco principal 

    # Abre conexão com o banco
    conexao = mysql.connector.connect(**CFG_BANCO)
    cursor = conexao.cursor()

    # Percorre cada cidade da lista
    for cidade in CIDADES:
        print(f"Buscando {cidade['nome']}...")

        # Chama a função que busca na API
        dados = buscar_clima(cidade["latitude"], cidade["longitude"])

        if dados:
            # Se retornou dados, salva no banco
            salvar_no_banco(cursor, cidade, dados)
            print(f"  {dados['temperatura']}°C | {dados['umidade']}% umidade | {dados['vento_kmh']} km/h")

    # Confirma todas as inserções de uma vez
    conexao.commit()

    cursor.close()
    conexao.close()
    print("Pronto! Rode agora: consultas.py")