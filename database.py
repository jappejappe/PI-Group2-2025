# database.py
import os
import psycopg2
from psycopg2.extras import RealDictCursor  # retorna dicionário ao invés de tupla
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "seu_usuario")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "sua_senha")
DB_PORT = os.environ.get("DB_PORT", "5432")


def _get_conn():
    return psycopg2.connect(
        host=DB_HOST,
        database="rcl_db",
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        client_encoding="UTF8"
    )


def get_anuncio_por_id(id_anuncio):
    if not id_anuncio:
        return None

    try:
        id_anuncio = int(id_anuncio)
    except (ValueError, TypeError):
        return None

    conn = _get_conn()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        SELECT a.id_anuncio, a.titulo_anuncio, tp.tipo, a.descricao_anuncio,
               c.condicao, a.quantidade_anuncio, a.preco_anuncio, f.foto
        FROM anuncios a
        JOIN tipos_produtos tp ON a.tipo_anuncio = tp.id_tipo
        JOIN condicoes_produtos c ON a.condicao_anuncio = c.id_condicao
        LEFT JOIN fotos_anuncios f ON a.id_anuncio = f.id_anuncio
        WHERE a.id_anuncio = %s
    """, (id_anuncio,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        return None

    anuncio_dict = {
        "id": rows[0]["id_anuncio"],
        "titulo": rows[0]["titulo_anuncio"],
        "tipo": rows[0]["tipo"],
        "descricao": rows[0]["descricao_anuncio"],
        "condicao": rows[0]["condicao"],
        "quantidade": rows[0]["quantidade_anuncio"],
        "preco": rows[0]["preco_anuncio"],
        "fotos": []
    }

    # adiciona todas as fotos
    for row in rows:
        # supondo row["foto"] == "foto_anuncio_1.png"
        if row["foto"]:
            anuncio_dict["fotos"].append(f"images/{row['foto']}")

    return anuncio_dict