# Bloco de Notas - Backend

Este projeto é a parte backend de um Bloco de Notas simples utilizando **Flask** e **SQLite**. Ele fornece uma API para adicionar, listar, editar e excluir notas, além de uma interface Swagger para documentação das rotas da API.

## Requisitos
Antes de começar, você precisa ter o Python e o `pip` instalados. Você pode verificar se o Python está instalado rodando:
python --version
Se o Python não estiver instalado, baixe e instale-o.

### Passo 1: Criar o ambiente virtual (venv)

Navegue até o diretório do projeto:
cd /caminho/para/o/projeto <br>
crie um ambiente virtual:<br>
python -m venv venv<br>

### Ative o ambiente virtual:

#### No Windows: 
venv\Scripts\activate
#### No macOS/Linux:
source venv/bin/activate

### Passo 2: Instalar as dependências
Com o ambiente virtual ativado, instale o Flask, o Flask-SQLAlchemy (para integração com o banco de dados SQLite) e o Flasgger (para documentação Swagger da API): <br>
pip install Flask Flask-SQLAlchemy flasgger

### Passo 4: Rodar o servidor
Inicie o servidor Flask:

Com o ambiente virtual ativado e as dependências instaladas, execute o comando abaixo para iniciar o servidor Flask:

python app.py

## Acesse a API:

Após iniciar o servidor, você pode acessar a API na URL http://127.0.0.1:5000/.

Swagger UI: Acesse a documentação da API via Swagger na URL http://127.0.0.1:5000/swagger.

## Rotas da API:
GET /notes: Lista todas as notas.<br>
POST /add_note: Adiciona uma nova nota.<br>
PUT /notes/<id>: Edita uma nota existente.<br>
DELETE /notes/<id>: Exclui uma nota.<br>

### Passo 5: Testando as rotas da API
Você pode usar ferramentas como Postman ou cURL para testar as rotas da API. Abaixo estão exemplos de como fazer as requisições:

#### Adicionar uma nova nota (POST):

Exemplo de corpo JSON:
                       
{
  "title": "Nova Nota",
  "description": "Descrição da nova nota"
}

**Requisição:**

curl -X POST http://127.0.0.1:5000/add_note -H "Content-Type: application/json" -d '{"title": "Nova Nota", "description": "Descrição da nova nota"}'


#### Listar todas as notas (GET): <br>
curl http://127.0.0.1:5000/notes

#### Editar uma nota (PUT):

Exemplo de corpo JSON:


{
  "title": "Nota Atualizada",
  "description": "Descrição atualizada"
}


**Requisição:**

curl -X PUT http://127.0.0.1:5000/notes/1 -H "Content-Type: application/json" -d '{"title": "Nota Atualizada", "description": "Descrição atualizada"}'


#### Excluir uma nota (DELETE):

curl -X DELETE http://127.0.0.1:5000/notes/1

