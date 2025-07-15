conteudo_env = '''
DB_HOST="localhost"
DB_NAME="postgres"
DB_USER="postgres"
DB_PASSWORD=""
DB_PORT="5432"
'''.strip()

with open('.env', 'w') as arquivo: # Caso não exista, já cria sozinho
    arquivo.write(conteudo_env)