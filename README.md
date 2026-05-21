# 🌤️ Mon Clima

Projeto Python que coleta dados climáticos em tempo real usando a API gratuita [Open-Meteo](https://open-meteo.com/) e armazena as informações em um banco de dados MySQL local.

---

## 📋 Funcionalidades

- Cria automaticamente o banco de dados e a tabela no MySQL
- Coleta dados climáticos de cidades via API Open-Meteo (sem necessidade de chave)
- Armazena temperatura, umidade, vento e localização no banco
- Permite consultas SQL aos dados coletados

---

## 🗂️ Estrutura do Projeto

```
mon_clima/
│
├── setup_banco.py       # Cria o banco de dados e a tabela no MySQL
├── coletar_clima.py     # Coleta os dados da API e insere no banco
├── consultas.py         # Realiza consultas ao banco de dados
└── README.md
```

---

## 🗃️ Estrutura do Banco de Dados

**Banco:** `mon_clima`  
**Tabela:** `registros_clima`

| Coluna         | Tipo           | Descrição                        |
|----------------|----------------|----------------------------------|
| id             | INT (PK, AI)   | Identificador único              |
| cidade         | VARCHAR(100)   | Nome da cidade                   |
| latitude       | FLOAT          | Latitude geográfica              |
| longitude      | FLOAT          | Longitude geográfica             |
| temperatura    | FLOAT          | Temperatura em °C                |
| umidade        | INT            | Umidade relativa em %            |
| vento_kmh      | FLOAT          | Velocidade do vento em km/h      |
| consultado_em  | DATETIME       | Data/hora da consulta (auto)     |

---

## ⚙️ Pré-requisitos

- Python 3.8+
- MySQL Server 8.x instalado e rodando
- Pacotes Python:

```bash
pip install mysql-connector-python requests
```

---

## 🚀 Como usar

### 1. Configure as credenciais do banco

Nos arquivos `setup_banco.py` e `coletar_clima.py`, edite o dicionário `CFG_BANCO`:

```python
CFG_BANCO = {
    "host": "localhost",
    "user": "root",
    "password": "SUA_SENHA_AQUI"
}
```

### 2. Crie o banco de dados

```bash
python setup_banco.py
```

### 3. Colete os dados climáticos

```bash
python coletar_clima.py
```

### 4. Faça consultas

```bash
python consultas.py
```

Ou abra o **MySQL Workbench** e execute:

```sql
SELECT * FROM mon_clima.registros_clima;
```

---

## 🌐 API Utilizada

[Open-Meteo](https://open-meteo.com/) — API meteorológica gratuita e open source, sem necessidade de cadastro ou chave de API.

---

## 📌 Observações

- Certifique-se de que o serviço MySQL está em execução antes de rodar os scripts.
- A coluna `consultado_em` é preenchida automaticamente com a data e hora da inserção.
- O projeto usa ambiente virtual (`.venv`) — recomendado ativá-lo antes de instalar dependências.

```bash
# Ativar ambiente virtual (Windows)
.venv\Scripts\activate

# Ativar ambiente virtual (Linux/Mac)
source .venv/bin/activate
```

---

## 👤 Autor

Paulo Minotto