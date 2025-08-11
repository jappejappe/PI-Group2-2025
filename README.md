# Projeto Integrador 2025

<p align="center">
    <img src="./images/recycle.gif" width="80px">
</p>



# **Descrição**
Com base no tema gerador proposto no Projeto Integrador 2025: "Fronteiras da Inovação: Intersecção da Ciência e Tecnologia para desenvolver soluções sustentáveis e inteligentes para os desafios globais" nós, do grupo 2, desenvolvemos o Recicla™ (RCL), um marketplace voltado para o comércio de sucatas e resíduos recicláveis, por conta do cenário atual e da escassez de opções acessíveis para vender esses materiais. O objetivo do Recicla é conectar catadores, cooperativas e pequenos geradores de resíduos a compradores de forma prática, incentivando a reciclagem e promovendo a sustentabilidade.
Confira também nosso [artigo científico](biorremediacao_de_polimeros_sinteticos.pdf).

<br><br>

# **Tecnologias e ferramentas**
<img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white"><img src="https://img.shields.io/badge/Figma-333230?style=for-the-badge&logo=figma&logoColor=red"><img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white"><img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css&logoColor=white"><img src="https://img.shields.io/badge/JavaScript-333230?style=for-the-badge&logo=javascript&logoColor=F7DF1E"><img src="https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"><img src="https://img.shields.io/badge/LaTeX-008080?style=for-the-badge&logo=latex&logoColor=white"><img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white">

<br><br>

# **Instalação**
## **Pré-requisitos**

<img src="https://img.shields.io/badge/Python-3.13%20+-blue?logo=python&logoColor=white"><img src="https://img.shields.io/badge/PiP-23.2.1%20+-blue?logo=pypi&logoColor=white"><img src="https://img.shields.io/badge/PSQL-17.5%20+-blue?logo=postgresql&logoColor=white">


## **Passo a passo**

Execute o arquivo `install_dependencies.bat`, o mesmo criará o arquivo `.env`, o qual deverá ser aberto e editado.

Você verá o seguinte:
```
DB_HOST="localhost"
DB_NAME="postgres"
DB_USER="postgres"
DB_PASSWORD=""
DB_PORT="5432"
```
Repare que o campo `DB_PASSWORD=""` está vazio. Preencha-o com a sua senha padrão do PostgreSQL e salve.

>***Nota:*** *Caso haja necessidade, altere as configurações como preferir.*

<br><br>
# Como utilizar
No terminal, já no diretório equivalente a raiz deste projeto, rode o `main.py` utilizando o _Python_.
```
python main.py
```
Acesse o link _http://127.0.0.1:5000_ exibido no terminal para navegar no site.

<br><br>
# Navegação
Para navegar entre as diferentes páginas do projeto, a equipe resolveu momentaneamente deixar este trabalho manual, ou seja, você precisa ver as rotas do *Flask* no arquivo `main.py`, e adicioná-las **manualmente** ao endereço da página.


*Exemplo de rota para o **login**:*
```
@app.route('/login')
```

*Como **você** deve deixar o endereço:*
```
http://127.0.0.1:5000/login
```