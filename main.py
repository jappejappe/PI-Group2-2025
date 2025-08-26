from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import psycopg2 as psql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import dotenv
import bcrypt

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
# Cria um cursor para executar comandos SQL

with connect.cursor() as cursor:
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", ('rcl_db',)) # Verifica se o 'rcl_db' já existe
    # pg_database é a tabela que contém os bancos de dados existentes no PostgreSQL
    # Retorna 1 se existir, caso contrário, retorna None

    dbExiste = cursor.fetchone() # Coleta o resultado da consulta
    print(dbExiste)

if dbExiste:
    print(f"Banco de dados 'rcl_db' já existe. Aguarde enquanto o mesmo é configurado.")
    connect.close()

else:
    with connect.cursor() as cursor:
        cursor.execute("CREATE DATABASE rcl_db;")
        connect.commit()
        connect.close()
        print(f"Banco de dados 'rcl_db' criado com sucesso. Aguarde enquanto o mesmo é configurado.")
    connect.close()


    connect = psql.connect(
        host=os.getenv("DB_HOST"),
        database="rcl_db",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )


    # Executa o script SQL para criar as tabelas
    with open("./data/database.sql", "r", encoding="utf-8") as cmd:
        sql = cmd.read().split(';')  # Divide o script em comandos individuais

    with connect.cursor() as cursor:
        for command in sql:
            if command.strip():  # Ignora comandos vazios
                cursor.execute(command)
    connect.commit()  # Confirma as alterações no banco de dados



dadosExemplo = input("Deseja pré-preencher o banco de dados com dados de exemplo? (s/n): ").strip().lower()
if dadosExemplo == 'n':
    print("Banco de dados não foi pré-preenchido com dados de exemplo.")
else: 
    with open("./data/add_dados.py", "r", encoding="utf-8") as cmd:
        os.system(f"python {cmd.name}")  # Executa o script para adicionar dados de exemplo

##################################################################



##################################################################
# ROTAS PARA CARREGAR PÁGINAS HTML
# As rotas abaixo são responsáveis por carregar os templates HTML,
# como: index.html, carrinho.html, registrar.html e login.html


app = Flask(__name__)
CORS(app)

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

@app.route('/perfil/<int:id_usuario>')
def perfil(id_usuario):
    connect = psql.connect(
        host=os.getenv("DB_HOST"),
        database="rcl_db",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    with connect.cursor() as cursor:
        # busca dados do usuario
        cursor.execute("""
            SELECT c.apelido_cliente, c.nome_cliente, u.id_comprador, u.id_vendedor
            FROM usuarios u
            JOIN compradores c ON u.id_comprador = c.id_comprador
            LEFT JOIN vendedores v ON u.id_vendedor = v.id_vendedor
            WHERE u.id_usuario = %s
        """, (id_usuario,))
        user = cursor.fetchone()

        if not user:
            return "Usuário não encontrado", 404

        apelido, nome, id_comprador, id_vendedor = user

        # busca anuncios caso usuario seja vendedor
        anuncios = []
        if id_vendedor:
            cursor.execute("""
                SELECT titulo_anuncio, descricao_anuncio, quantidade_anuncio, preco_anuncio
                FROM anuncios
                WHERE id_vendedor = %s
            """, (id_vendedor,))
            anuncios = cursor.fetchall()

    connect.close()

    # define a funcao do usuario
    funcoes = []
    if id_comprador: funcoes.append("Comprador")
    if id_vendedor: funcoes.append("Vendedor")
    funcao_str = "/".join(funcoes) if funcoes else "Usuário"

    return render_template(
        'pages/perfil.html',
        apelido=apelido,
        nome=nome,
        funcao=funcao_str,
        anuncios=anuncios
    )

@app.route('/compra') # Rota para compra
def compra():
    return render_template('pages/compra.html')

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



@app.route("/registrarDB", methods=["POST"])
def registrarDB():
    data = request.json
    connect = psql.connect(
        host=os.getenv("DB_HOST"),
        database="rcl_db",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    try:
        password = data.get("password")
        senha_bytes = password.encode('utf-8') # trasforma a senha em bytes
        hash_senha = bcrypt.hashpw(senha_bytes, bcrypt.gensalt()) # pega a senha em bytes, "mistura" com o salt e gera o hash
        hash_str = hash_senha.decode('utf-8') # transforma o hash em string pra salvar no campo senha que é varchar
        print(hash_str)

        with connect.cursor() as cursor:
            cursor.execute(
                """
                    INSERT INTO compradores (nome_cliente, apelido_cliente, email_cliente, data_nascimento, cep_cliente, cpf_cliente, senha)
                    VALUES (%(nome)s, %(apelido)s, %(email)s, %(nascimento)s, %(cep)s, %(cpf)s, %(password)s)
                    RETURNING id_comprador;
                """,
                # retorna o id do novo vendedor inserido
            {
                "nome": data.get("nome"),
                "apelido": data.get("apelido"),
                "email": data.get("email"),
                "nascimento": data.get("nascimento"),
                "cep": data.get("cep"),
                "cpf": data.get("cpf"),
                "password": hash_str
            }
            )
            new_id = cursor.fetchone()[0] # coleta o id do novo comprador inserido

            cursor.execute(
                """
                    INSERT INTO usuarios (id_comprador) VALUES (%s);
                """,
                (new_id,)
            )

        connect.commit()
        connect.close()
        return jsonify({"status": "Sucesso", "message": "Usuário adicionado", "id": new_id})
    except Exception as e:
        connect.rollback()
        return jsonify({"status": "Falha", "message": "Usuário não adicionado", "error": str(e)})
    
@app.route("/cadastrarVendedor", methods=["POST"])
def cadastrarVendedor():
    data = request.json
    connect = psql.connect(
        host=os.getenv("DB_HOST"),
        database="rcl_db",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    try:
        with connect.cursor() as cursor:
            cursor.execute(
                """
                    INSERT INTO vendedores (id_comprador, nome_empresa, email_empresa, cep_empresa, telefone_empresa, descricao_empresa)
                    VALUES (%(id_comprador)s, %(nome)s, %(email)s, %(cep)s, %(telefone)s, %(descricao)s)
                    RETURNING id_vendedor;
                """,
                # retorna o id do novo vendedor inserido
                {
                    "id_comprador": data.get("id_comprador"),
                    "nome": data.get("nome"),
                    "email": data.get("email"),
                    "cep": data.get("cep"),
                    "telefone": data.get("telefone"),
                    "descricao": data.get("descricao")
                }
            )

            new_id = cursor.fetchone()[0] # coleta o id do novo vendedor inserido
            id_comprador = data.get("id_comprador")

            cursor.execute(
                """
                    UPDATE usuarios SET id_vendedor = %s WHERE id_comprador = %s;
                """,
                (new_id, id_comprador)
            )

        connect.commit()
        connect.close()
        return jsonify({"status": "Sucesso", "message": "Vendedor adicionado"})
    except Exception as e:
        connect.rollback()
        return jsonify({"status": "Falha", "message": "Usuário não adicionado", "error": str(e)})
    
@app.route("/logar", methods=["POST"])
def logar():
    data = request.json
    connect = psql.connect(
        host=os.getenv("DB_HOST"),
        database="rcl_db",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    try:
        with connect.cursor() as cursor:
            cursor.execute(
                """
                    SELECT email_cliente, senha, id_comprador FROM compradores WHERE email_cliente = %(email)s
                """, 
                {
                    "email": data.get("email"),
                })
            
            user = cursor.fetchone() # tupla (email, senha)
            if user is None:
                return jsonify({"status": "Falha", "message": "Usuário não encontrado"})
            

            if bcrypt.checkpw(data.get("password").encode("utf-8"), user[1].encode("utf-8")):
                print("Senha correta")
                return jsonify({"status": "Sucesso", "message": "Login efetuado", "compradorId": user[2]})
            else:
                print("Senha incorreta")
                return jsonify({"status": "Falha", "message": "Senha incorreta"})
            

            
    except Exception as e:
        connect.rollback()
        return jsonify({"status": "Falha", "message": "Erro ao tentar logar", "error": str(e)})
        
        


##################################################################


# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)