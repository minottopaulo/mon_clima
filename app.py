from flask import Flask, render_template, request, jsonify
import mysql.connector
import requests
from datetime import datetime

app = Flask(__name__)

CFG_BANCO = {
    "host":     "localhost",
    "user":     "root",
    "password": "1532",
    "database": "mon_clima"
}

def get_db():
    return mysql.connector.connect(**CFG_BANCO)


@app.route("/")
def index():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    #contagem de registros do bancos 
    cursor.execute("SELECT COUNT(*) as total FROM registros_clima")
    total = cursor.fetchone()["total"]
    #calculo da media da temperatura de todos os registros 
    cursor.execute("SELECT ROUND(AVG(temperatura), 1) as temp_media FROM registros_clima")
    row = cursor.fetchone()
    temp_media = row["temp_media"] if row and row["temp_media"] else 0
    #busca a cidade que mais busca no banco de dados 
    cursor.execute("""
    SELECT cidade, COUNT(*) as total FROM registros_clima
    GROUP BY cidade ORDER BY total DESC LIMIT 1
    """)
    row = cursor.fetchone()
    cidade_top = row["cidade"] if row else "—"
    #busca a data e hora mais recente do registro 
    cursor.execute("SELECT consultado_em FROM registros_clima ORDER BY consultado_em DESC LIMIT 1")
    row = cursor.fetchone()
    ultima = row["consultado_em"].strftime("%d/%m/%Y %H:%M") if row else "—"
    # Dados para gráfico (últimos 20 registros)
    cursor.execute("""
        SELECT cidade, temperatura, umidade, vento_kmh, consultado_em
        FROM registros_clima ORDER BY consultado_em DESC LIMIT 20
    """)
    registros_grafico = cursor.fetchall()
    # Tabela (todos)
    cursor.execute("SELECT * FROM registros_clima ORDER BY consultado_em DESC")
    registros = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html",
        total=total,
        temp_media=temp_media,
        cidade_top=cidade_top,
        ultima=ultima,
        registros=registros,
        registros_grafico=registros_grafico
    )
 
# ── Buscar clima de uma cidade ────────────────────────────────────────────────
@app.route("/buscar", methods=["POST"])
def buscar():
    cidade = request.form.get("cidade", "").strip()
    if not cidade:
        return jsonify({"erro": "Informe o nome da cidade."}), 400
 
    # Geocoding com Open-Meteo
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={cidade}&count=1&language=pt"
    geo = requests.get(geo_url, timeout=10).json()
 
    if not geo.get("results"):
        return jsonify({"erro": f"Cidade '{cidade}' não encontrada."}), 404
 
    result = geo["results"][0]
    lat = result["latitude"]
    lon = result["longitude"]
    nome = result["name"]
 
    # Clima
    clima_url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current_weather=true"
        f"&hourly=relativehumidity_2m"
        f"&timezone=auto"
    )
    clima = requests.get(clima_url, timeout=10).json()
    cw = clima["current_weather"]
    temp = cw["temperature"]
    vento = cw["windspeed"]
    umidade = clima["hourly"]["relativehumidity_2m"][0]
 
    # Salvar no banco
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO registros_clima (cidade, latitude, longitude, temperatura, umidade, vento_kmh)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nome, lat, lon, temp, umidade, vento))
    conn.commit()
    cursor.close()
    conn.close()
 
    return jsonify({
        "cidade": nome,
        "temperatura": temp,
        "umidade": umidade,
        "vento_kmh": vento,
        "latitude": lat,
        "longitude": lon,
        "hora": datetime.now().strftime("%d/%m/%Y %H:%M")
    })
# ── API: dados para gráfico ───────────────────────────────────────────────────
@app.route("/api/grafico")
def api_grafico():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT cidade, temperatura, umidade, vento_kmh,
            DATE_FORMAT(consultado_em, '%d/%m %H:%i') as hora
        FROM registros_clima ORDER BY consultado_em DESC LIMIT 20
    """)
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(dados[::-1])  # cronológico

if __name__ == "__main__":
    app.run(debug=True)