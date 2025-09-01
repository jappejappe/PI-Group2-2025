from flask import Flask, render_template, request, jsonify, send_from_directory, session, redirect, url_for
from flask_cors import CORS
import os
import json
import psycopg2 as psql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import dotenv
import bcrypt
import base64
from database import get_anuncio_por_id

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
app.secret_key = 'sua_chave_secreta_aqui'  # Necessário para usar sessões
CORS(app)

@app.route('/') # Rota principal que carrega o index.html
def home():
    return render_template('pages/index.html')


@app.route('/carrinho')
def carrinho():
    comprador_id = session.get("compradorId")
    
    # Se não há comprador logado, redireciona para login
    if not comprador_id:
        return redirect(url_for('login'))
    
    connect = psql.connect(
        host=os.getenv("DB_HOST"),
        database="rcl_db",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    itens = []
    try:
        with connect.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    a.id_anuncio, 
                    a.titulo_anuncio, 
                    a.preco_anuncio, 
                    COALESCE(f.foto, '/static/images/residuos1.jpg') as foto,
                    c.quantidade,
                    COALESCE(v.nome_empresa, 'Loja RCL') as nome_empresa
                FROM carrinhos c
                JOIN anuncios a ON c.id_produto = a.id_anuncio
                LEFT JOIN vendedores v ON a.id_vendedor = v.id_vendedor
                LEFT JOIN fotos_anuncios f ON a.id_anuncio = f.id_anuncio
                WHERE c.id_comprador = %s
                ORDER BY a.id_anuncio
            """, (comprador_id,))
            itens = cursor.fetchall()
    finally:
        connect.close()

    return render_template('pages/carrinho.html', itens=itens)


@app.route('/registrar') # Rota para registrar um novo usuário
def registrar():
    return render_template('pages/registrar.html')


@app.route('/login') # Rota para login
def login():
    return render_template('pages/login.html')

@app.route('/logout') # Rota para logout
def logout():
    session.clear()  # Limpa toda a sessão
    return redirect(url_for('home'))

@app.route('/anunciar') # Rota para anunciar
def anunciar():
    return render_template('pages/anunciar.html')

@app.route('/anuncio') # Rota para anúncio
def anuncio():
    id_anuncio = request.args.get('id')
    if not id_anuncio:
        return "ID do anúncio não fornecido", 400

    anuncio_data = get_anuncio_por_id(id_anuncio)
    if not anuncio_data:
        return "Anúncio não encontrado", 404

    return render_template('pages/anuncio.html', anuncio=anuncio_data)

# rota de teste para checar conexão ao banco rapidamente
@app.route('/_testdb')
def testdb():
    try:
        a = get_anuncio_por_id(1)  # teste com id 1
        return {"ok": True, "exemplo": bool(a)}
    except Exception as e:
        return {"ok": False, "erro": str(e)}, 500

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
            SELECT c.apelido_cliente, c.nome_cliente, c.foto, u.id_comprador, u.id_vendedor
            FROM usuarios u
            JOIN compradores c ON u.id_comprador = c.id_comprador
            LEFT JOIN vendedores v ON u.id_vendedor = v.id_vendedor
            WHERE u.id_usuario = %s
        """, (id_usuario,))
        user = cursor.fetchone()

        if not user:
            return "Usuário não encontrado", 404

        apelido, nome, foto, id_comprador, id_vendedor = user

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
        foto=foto,
        funcao=funcao_str,
        anuncios=anuncios
    )

@app.route('/compra') # Rota para compra
def compra():
    comprador_id = session.get("compradorId")
    
    # se nao está logado, vai pro login
    if not comprador_id:
        return redirect(url_for('login'))
    
    connect = psql.connect(
        host=os.getenv("DB_HOST"),
        database="rcl_db",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    
    itens_carrinho = []
    total_compra = 0.0  # Garante que seja float
    
    try:
        with connect.cursor() as cursor:
            # busca itens do carrinho
            cursor.execute("""
                SELECT 
                    a.id_anuncio, 
                    a.titulo_anuncio, 
                    a.preco_anuncio, 
                    ARRAY_AGG(f.foto) as fotos,
                    c.quantidade,
                    v.nome_empresa
                FROM carrinhos c
                JOIN anuncios a ON c.id_produto = a.id_anuncio
                LEFT JOIN vendedores v ON a.id_vendedor = v.id_vendedor
                LEFT JOIN fotos_anuncios f ON a.id_anuncio = f.id_anuncio
                WHERE c.id_comprador = %s
                GROUP BY a.id_anuncio, a.titulo_anuncio, a.preco_anuncio, c.quantidade, v.nome_empresa
            """, (comprador_id,))
            
            itens_carrinho = cursor.fetchall()
            
            # calcula total
            for item in itens_carrinho:
                total_compra += float(item[2]) * item[4]
                
    finally:
        connect.close()

    return render_template('pages/compra.html', itens=itens_carrinho, total=total_compra)

##################################################################




##################################################################
# ENDPOINTS PARA MANIPULAÇÃO DE DADOS
# Os endpoints abaixo são responsáveis por manipular dados,
# como adicionar itens ao carrinho ou publicar um novo produto.

@app.route("/getCarrinho", methods=["POST"])
def getCarrinho():
    data = request.get_json()
    comprador_id = data.get("id_comprador")
    
    if not comprador_id:
        return jsonify({"status": "erro", "mensagem": "ID do comprador não fornecido"}), 400

    conn = psql.connect(
        host=os.getenv("DB_HOST"),
        database="rcl_db",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT a.id_anuncio, a.titulo_anuncio, a.preco_anuncio, c.quantidade
                FROM carrinhos c
                JOIN anuncios a ON c.id_produto = a.id_anuncio
                WHERE c.id_comprador = %s
            """, (comprador_id,))
            itens = cursor.fetchall()
        conn.close()

        lista = []
        for id_anuncio, titulo, preco, qtd in itens:
            lista.append({
                "id": id_anuncio,
                "titulo": titulo,
                "preco": float(preco),  # Garante que o preço seja float
                "quantidade": qtd
            })

        return jsonify(lista)

    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

@app.route("/addCarrinho", methods=["POST"])
def adicionar_carrinho():
    data = request.get_json()
    id_comprador = data["id_comprador"]
    id_produto = data["id_produto"]
    quantidade = data.get("quantidade", 1)

    conn = psql.connect(
        host=os.getenv("DB_HOST"),
        database="rcl_db",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT quantidade FROM carrinhos
                WHERE id_comprador = %s AND id_produto = %s
            """, (id_comprador, id_produto))
            existe = cursor.fetchone()

            if existe:
                nova_qtd = existe[0] + quantidade
                cursor.execute("""
                    UPDATE carrinhos
                    SET quantidade = %s
                    WHERE id_comprador = %s AND id_produto = %s
                """, (nova_qtd, id_comprador, id_produto))
            else:
                cursor.execute("""
                    INSERT INTO carrinhos (id_comprador, id_produto, quantidade)
                    VALUES (%s, %s, %s)
                """, (id_comprador, id_produto, quantidade))

        conn.commit()
        return jsonify({"status": "ok"})
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)})
    finally:
        conn.close()



@app.route("/registrarDB", methods=["POST"])
def registrarDB():
    data = request.get_json()
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

        with connect.cursor() as cursor:
            cursor.execute(
                """
                    INSERT INTO compradores (nome_cliente, apelido_cliente, email_cliente, data_nascimento, cep_cliente, cpf_cliente, senha, foto)
                    VALUES (%(nome)s, %(apelido)s, %(email)s, %(nascimento)s, %(cep)s, %(cpf)s, %(password)s, %(foto)s)
                    RETURNING id_comprador;
                """,
                # retorna o id do novo comprador inserido
            {
                "nome": data.get("nome"),
                "apelido": data.get("apelido"),
                "email": data.get("email"),
                "nascimento": data.get("nascimento"),
                "cep": data.get("cep").replace("-", ""),
                "cpf": data.get("cpf", "").replace(".", "").replace("-", ""),
                "password": hash_str,
                "foto": data.get("foto")
            }
            )
            compradorId = cursor.fetchone()[0] # coleta o id do novo comprador inserido

            cursor.execute(
                """
                    INSERT INTO usuarios (id_comprador) VALUES (%s);
                """,
                (compradorId,)
            )

            cursor.execute(
                """
                    SELECT id_usuario FROM usuarios WHERE id_comprador = (%s);
                """,
                (compradorId,)
            )
            usuarioId = cursor.fetchone()[0]

        connect.commit()
        session["compradorId"] = compradorId  # Salva o compradorId na sessão
        return jsonify({"status": "Sucesso", "message": "Usuário adicionado", "compradorId": compradorId, "usuarioId": usuarioId}), 200
    except Exception as e:
        connect.rollback()
        return jsonify({"status": "Falha", "message": "Usuário não adicionado", "error": str(e)})
    finally:
        if connect:
            connect.close()
    
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
        cep = data.get("cep", "").replace("-", "").strip()
        telefone = data.get("telefone", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "").strip()

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
                    "cep": cep,
                    "telefone": telefone,
                    "descricao": data.get("descricao")
                }
            )

            id_vendedor = cursor.fetchone()[0] # coleta o id do novo vendedor inserido
            carregamentos = data.get("carregamentos", [])

            for carregamento in carregamentos:
                cursor.execute(
                    """
                        INSERT INTO vendedores_carregamento (id_vendedor, id_carregamento)
                        VALUES (%s, %s) 
                    """,
                    (
                        id_vendedor, int(carregamento)
                    )
                )

            cursor.execute(
                """
                    UPDATE usuarios SET id_vendedor = %s WHERE id_comprador = %s;
                """,
                (id_vendedor, data.get("id_comprador"))
            )

        connect.commit()
        connect.close()
        return jsonify({"status": "Sucesso", "message": "Vendedor adicionado", "vendedorId": id_vendedor})
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
                session["compradorId"] = user[2]  # Salva o compradorId na sessão
                return jsonify({"status": "Sucesso", "message": "Login efetuado", "compradorId": user[2]})
            else:
                print("Senha incorreta")
                return jsonify({"status": "Falha", "message": "Senha incorreta"})
            

            
    except Exception as e:
        connect.rollback()
        return jsonify({"status": "Falha", "message": "Erro ao tentar logar", "error": str(e)})
        
@app.route("/mostrarAnuncios", methods=["POST", "GET"])
def mostrarAnuncios():
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
                    SELECT id_anuncio, titulo_anuncio, preco_anuncio FROM anuncios;
                """
            )
            anuncios = cursor.fetchall() # lista dos anúncios (tuplas)
        connect.close()

        lista_anuncios = []
        for anuncio in anuncios:
            lista_anuncios.append({
                "id": anuncio[0],
                "titulo": anuncio[1],
                "preco": int(anuncio[2])
            })

        return jsonify(lista_anuncios)
    
    except Exception as e:
        connect.rollback()
        connect.close()
        return f"Erro ao carregar anúncios: {str(e)}"
    

@app.route("/salvarImagens", methods=["POST"])
def salvarImagens():
    data = request.get_json()
    connect = psql.connect(
        host=os.getenv("DB_HOST"),
        database="rcl_db",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    try:
        titulo = data.get("titulo")
        condicao = int(data.get("condicao"))
        tipo_material = int(data.get("tipo_material"))
        descricao = data.get("descricao")
        quantidade = int(data.get("quantidade"))
        preco = int(data.get("preco"))
        imagens = data.get("imagens", [])
        comprador_id = int(data.get("compradorId"))

        with connect.cursor() as cursor:
            cursor.execute("SELECT id_vendedor FROM vendedores WHERE id_comprador = %s", (comprador_id,))
            vendedor_result = cursor.fetchone()
            
            if not vendedor_result:
                return jsonify({"status": "Erro", "message": "Usuário não está cadastrado como vendedor"}), 400
            
            id_vendedor = vendedor_result[0]
            
            cursor.execute(
                """
                    INSERT INTO anuncios (titulo_anuncio, tipo_anuncio, descricao_anuncio, condicao_anuncio, quantidade_anuncio, preco_anuncio, id_vendedor)
                    VALUES (%(titulo)s, %(tipo_material)s, %(descricao)s, %(condicao)s, %(quantidade)s, %(preco)s, %(id_vendedor)s)
                    RETURNING id_anuncio;
                """,
                {
                    "titulo": titulo,
                    "tipo_material": tipo_material,
                    "descricao": descricao,
                    "condicao": condicao,
                    "quantidade": quantidade,
                    "preco": preco,
                    "id_vendedor": id_vendedor,
                }
            )

            id_anuncio = cursor.fetchone()[0]

            for img_base64 in imagens:
                cursor.execute(
                    """
                        INSERT INTO fotos_anuncios (id_anuncio, foto)
                        VALUES (%(id_anuncio)s, %(imagem_base64)s);
                    """,
                    {
                        "id_anuncio": id_anuncio,
                        "imagem_base64": img_base64
                    }
                )

        connect.commit()

        return jsonify({"status": "Sucesso", "message": f"Título: {titulo}, Condição: {condicao}, Tipo de material: {tipo_material}, Descrição: {descricao}, Quantidade: {quantidade}, Preço: {preco}, Imagens recebidas: {len(imagens)}"})

    except Exception as e:
        connect.rollback()
        print("erro:", str(e))
        return jsonify({"status": "Erro", "message": str(e)}), 500
    finally:
        connect.close()

##################################################################


# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)