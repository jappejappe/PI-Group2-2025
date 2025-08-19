import os
import psycopg2 as psql
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

compradores = [
    ("Pietro Matheus", "mezzo", "mezzo@gmail.com", "2000-08-26", "12345678", "11111111111", "senhasegura"),
    ("Bruno Costa", "brunoc", "bruno@gmail.com", "1999-02-16", "87654321", "22222222222", "bruno2452"),
    ("Carla Souza", "carlas", "carla@gmail.com", "2001-01-22", "12121212", "33333333333", "bananapimentinha"),
    ("Daniel Lima", "danlima", "daniel@gmail.com", "1998-09-29", "32323232", "44444444444", "biscoito80vinte"),
    ("Eduarda Rocha", "duda", "eduarda@gmail.com", "2002-09-07", "12312312", "55555555555", "password"),
    ("Felipe Alves", "felipea", "felipe@gmail.com", "1997-11-02", "12345432", "66666666666", "senha"),
    ("Isabela Martins", "isa", "isa@gmail.com", "2003-03-15", "11223344", "77777777777", "99trinta"),
]

for c in compradores:
    cursor.execute("""
        INSERT INTO compradores (nome_cliente, apelido_cliente, email_cliente, data_nascimento, cep_cliente, cpf_cliente, senha)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (apelido_cliente, email_cliente, cpf_cliente) DO NOTHING;
    """, c)


vendedores = [
    ("12345678", "Sucatos Ltda", "47988887777", "eco@sucata.com", "Compra e venda de sucatas", 1),
    ("87654321", "Recicla", "47999998888", "corp@recicla.com", "Reciclagem de plásticos", 2),
    ("12121212", "Garrafalandia", "47977776666", "garrafas@market.com", "Coleta de garrafas de vidro", 3),
]

for v in vendedores:
    cursor.execute("""
        INSERT INTO vendedores (cep_empresa, nome_empresa, telefone_empresa, email_empresa, descricao_empresa, id_comprador)
        VALUES (%s,%s,%s,%s,%s,%s)
        ON CONFLICT (id_vendedor, email_empresa, telefone_empresa, id_comprador) DO NOTHING;
    """, v)


tipos = ["Garrafas de Vidro", "Plástico", "Papelão", "Alumínio", "Ferro Velho", "Cobre", "Eletrônicos"]
for t in tipos:
    cursor.execute("""
        INSERT INTO tipos_produtos (tipo) VALUES (%s)
        ON CONFLICT (tipo, id_tipo) DO NOTHING;
    """, (t,))


condicoes = ["Excelente", "Bom", "Usado", "Danificado"]
for c in condicoes:
    cursor.execute("""
        INSERT INTO condicoes_produtos (condicao) VALUES (%s)
        ON CONFLICT (id_condicao, condicao) DO NOTHING;
    """, (c,))


carregamentos = ["Caminhão", "Carreta", "Van", "Carro", "Kombi"]
for c in carregamentos:
    cursor.execute("""
        INSERT INTO carregamentos (carregamento) VALUES (%s)
        ON CONFLICT (id_carregamento, carregamento) DO NOTHING;
    """, (c,))


vendedores_carregamento = [
    (1, 1), (1, 4),
    (2, 2), (2, 5),
    (3, 3), (3, 4),
]
for vc in vendedores_carregamento:
    cursor.execute("""
        INSERT INTO vendedores_carregamento (id_vendedor, id_carregamento)
        VALUES (%s,%s);
    """, vc)


usuarios = [
    (1, 1), (2, 2), (3, 3),  # compradores que também são vendedores
    (4, None), (5, None), (6, None), (7, None)
]
for u in usuarios:
    cursor.execute("""
        INSERT INTO usuarios (id_comprador, id_vendedor)
        VALUES (%s,%s)
        ON CONFLICT (id_usuario, id_vendedor, id_comprador) DO NOTHING;
    """, u)


anuncios = [
    ("Garrafas de vidro transparentes", 1, "Garrafas usadas, 50 unid.", 3, 50, 8, 1),
    ("Garrafas de cerveja verdes", 1, "100 garrafas retornáveis", 2, 100, 5, 3),
    ("Garrafas marrons diversas", 1, "80 garrafas marrons", 3, 80, 4, 3),
    ("Plásticos PET variados", 2, "Plástico PET prensado", 2, 200, 3, 2),
    ("Plásticos coloridos", 2, "Plástico PEAD triturado", 1, 150, 3, 2),
    ("Plástico filme", 2, "Plástico filme esticável", 3, 120, 3, 1),
    ("Papelão prensado", 3, "Fardos de papelão limpo", 2, 100, 3, 3),
    ("Caixas de papelão grandes", 3, "Caixas desmontadas", 3, 50, 2, 2),
    ("Latas de alumínio", 4, "Latas prensadas", 2, 300, 4, 1),
    ("Alumínio em chapas", 4, "Sobras industriais", 3, 30, 6, 1),
    ("Ferro velho", 5, "Ferro e aço enferrujados", 4, 500, 3, 2),
    ("Ferro pesado", 5, "Peças pesadas de ferro", 4, 1000, 4, 2),
    ("Sucata de cobre", 6, "Fios de cobre soltos", 1, 50, 25, 1),
    ("Cobre", 6, "Sucata mista de cobre", 3, 70, 30, 1),
    ("Eletrônicos para descarte", 7, "PCs e placas sem uso", 4, 25, 6, 3),
]
for a in anuncios:
    cursor.execute("""
        INSERT INTO anuncios (titulo_anuncio, tipo_anuncio, descricao_anuncio, condicao_anuncio, quantidade_anuncio, preco_anuncio, id_vendedor)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (id_anuncio) DO NOTHING;
    """, a)

carrinhos = [
    (4, 1, 5),
    (4, 4, 2),
    (5, 9, 6),
    (6, 13, 1),
]
for c in carrinhos:
    cursor.execute("""
        INSERT INTO carrinhos (id_comprador, id_produto, quantidade)
        VALUES (%s,%s,%s);
    """, c)

fotos = [(i, f"foto_anuncio_{i}.png") for i in range(1, 16)]
for f in fotos:
    cursor.execute("""
        INSERT INTO fotos_anuncios (id_anuncio, foto)
        VALUES (%s,%s)
        ON CONFLICT (id_foto) DO NOTHING;
    """, f)

connect.commit()
cursor.close()
connect.close()

print("Adicionado dados fictícios ao banco.")
