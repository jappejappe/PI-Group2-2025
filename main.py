from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
import psycopg2 as psql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import dotenv

#################################################################
# CARREGAMENTO DE VARIÁVEIS DE AMBIENTE
# Carrega as variáveis de ambiente do arquivo .env
dotenv.load_dotenv()
##################################################################



#################################################################
# CONFIGURAÇÃO DO BANCO DE DADOS
# Aqui você deve configurar a conexão com o banco de dados PostgreSQL.

connect = psql.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

connect.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # Define a permissão pra criar bancos de dados
cursor = connect.cursor() # Cria um cursor para executar comandos SQL


cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", ('rcl_db',)) # Verifica se o 'rcl_db' já existe
# pg_database é a tabela que contém os bancos de dados existentes no PostgreSQL
# Retorna 1 se existir, caso contrário retorna None

dbExiste = cursor.fetchone() # Coleta o resultado da consulta

if dbExiste:
    print(f"Banco de dados 'rcl_db' já existe. Aguarde enquanto o mesmo é configurado.")

else:
    cursor.execute("CREATE DATABASE rcl_db;")
    print(f"Banco de dados 'rcl_db' criado com sucesso. Aguarde enquanto o mesmo é configurado.")
    connect.close()

    connect = psql.connect( # Conecta no banco 'rcl_db'
        host=os.getenv("DB_HOST"),
        database="rcl_db",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    cursor = connect.cursor()


    # Executa o script SQL para criar as tabelas
    with open("./data/database.sql", "r", encoding="utf-8") as cmd:
        sql = cmd.read()

    cursor.execute(sql)

connect.commit()


dadosExemplo = input("Deseja pré-preencher o banco de dados com dados de exemplo? (s/n): ").strip().lower()
if dadosExemplo == 'n':
    connect.close()
else: 
    with open("./data/add_dados.py", "r", encoding="utf-8") as cmd:
        os.system(f"python {cmd.name}")  # Executa o script para adicionar dados de exemplo

##################################################################



##################################################################
# ROTAS PARA CARREGAR PÁGINAS HTML
# As rotas abaixo são responsáveis por carregar os templates HTML,
# como: index.html, carrinho.html, registrar.html e login.html


app = Flask(__name__)

@app.route('/') # Rota principal que carrega o index.html
def home():
    return render_template('pages/index.html')


@app.route('/carrinho') # Rota para o carrinho
def carrinho():
    return render_template('pages/carrinho.html')


@app.route('/registrar') # Rota para registrar um novo usuário
def registrar():
    return render_template('pages/registrar.html')


@app.route('/login') # Rota para login
def login():
    return render_template('pages/login.html')

@app.route('/anunciar') # Rota para anunciar
def anunciar():
    return render_template('pages/anunciar.html')

@app.route('/anuncio') # Rota para anúncio
def anuncio():
    return render_template('pages/anuncio.html')

@app.route('/cadastroVendedor') # Rota para cadastrar vendedor
def cadastroVendedor():
    return render_template('pages/cadastroVendedor.html')

@app.route('/perfil') # Rota para perfil
def perfil():
    return render_template('pages/perfil.html')

##################################################################




##################################################################
# ENDPOINTS PARA MANIPULAÇÃO DE DADOS
# Os endpoints abaixo são responsáveis por manipular dados,
# como adicionar itens ao carrinho ou publicar um novo produto.


@app.route('/addCarrinho', methods=['POST']) # Endpoint acionado para adicionar itens ao carrinho
def addCarrinho():
    data = request.get_json()
    with open('data.json', 'w') as f: # Abre o data.json para escrita ('w' write)
        json.dump(data, f)
    return jsonify({'status': 'success'})


##################################################################


# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)