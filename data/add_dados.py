import os
import psycopg2 as psql
from datetime import date
import dotenv

dotenv.load_dotenv()

connect = psql.connect(
    host=os.getenv("DB_HOST"),
    database="rcl_db",
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

cursor = connect.cursor()

# inserir 10 usuarios na tabela
usuarios = [
    ("Pietro Matheus", "mezzo", "mezzo@gmail.com", "2008-08-26", "12345678", "11111111111", "senhasegura"),
    ("Bruno Costa", "brunoc", "bruno@gmail.com", "2008-02-16", "87654321", "22222222222", "bruno2452"),
    ("Carla Souza", "carlas", "carla@gmail.com", "2008-01-22", "12121212", "33333333333", "bananapimentinha"),
    ("Daniel Lima", "danlima", "daniel@gmail.com", "2008-09-29", "32323232", "44444444444", "biscoito80vinte"),
    ("Eduarda Rocha", "duda", "eduarda@gmail.com", "2008-09-07", "12312312", "55555555555", "password"),
    ("Felipe Alves", "felipea", "felipe@gmail.com", "2008-11-02", "12345432", "66666666666", "senha"),
    ("Ricardo Noel", "santa", "noel@gmail.com", "1270-12-25", "11121112", "77777777777", "sabonete"),
    ("Henrique Souza", "henri", "henrique@gmail.com", "2008-08-26", "09060906", "88888888888", "oitooito8"), # falta ainda
    ("Isabela Martins", "isa", "isa@gmail.com", "2008-08-26", "11223344", "99999999999", "99trinta"),       # identificar uns 3
    ("Joao Pedro", "jp", "joao@gmail.com", "2008-08-26", "12012069", "00000000000", "senhazinha321"),        # como vendedores
]

for u in usuarios:
    cursor.execute("""
        INSERT INTO users (nome, username, email, nascimento, cep, cpf, password)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (email) DO NOTHING;
    """, u)


# inserir os tipos de produtos
tipos = ["Eletrônico", "Roupas", "Livros", "Móveis", "Esporte"]
for t in tipos:
    cursor.execute("""
        INSERT INTO tipos_produtos (tipo) VALUES (%s)
        ON CONFLICT (tipo) DO NOTHING;
    """, (t,))


# inserir produtos de cada tipo
produtos = [
    ("Eletronico", "Smartphone"),
    ("Eletronico", "Notebook"),
    ("Eletronico", "Fone de Ouvido"),
    ("Roupas", "Camiseta SOAD"),
    ("Roupas", "Touca de Tigre"),
    ("Roupas", "Tenis Nike"),
    ("Livros", "Cafe com Deus Pai"),
    ("Livros", "Diario de um Banana"),
    ("Livros", "A Divina Comedia"),
    ("Moveis", "Pintura Noite Estrelada"),
    ("Moveis", "Mesa de Escritorio"),
    ("Moveis", "Estante de Livros"),
    ("Esporte", "Bola de Futebol"),
    ("Esporte", "Bicicleta"),
    ("Esporte", "Raquete de Tenis"),
]

for p in produtos:
    cursor.execute("""
        INSERT INTO produtos (tipo_produto, nome) VALUES (%s, %s)
    """, p)

connect.commit()
cursor.close()
connect.close()

print("Adicionado dados ao banco.")
