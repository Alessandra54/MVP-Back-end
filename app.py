from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

# Inicializando o Flask
app = Flask(
    __name__,
    template_folder='../front_end/templates',
    static_folder='../front_end/static'
)

# Configuração do Swagger
swagger_config = {
    "swagger": "2.0",
    "info": {
        "title": "API de Notas",
        "description": "Documentação das rotas da API para gerenciar notas",
        "version": "1.0.0",
    },
    "host": "localhost:5000",
    "basePath": "/",
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # Inclui todas as rotas
            "model_filter": lambda tag: True,  # Inclui todos os modelos
        }
    ],
    "headers": []  # Configuração padrão para evitar erro
}

# Inicializando o Swagger
Swagger(app, config=swagger_config)

# Configuração do banco de dados (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicia o banco de dados
db = SQLAlchemy(app)

# Define o modelo de Nota
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)

# Criação do banco de dados
with app.app_context():
    db.create_all()

# Rota para a página inicial (site)
@app.route('/')
def home():
    return render_template('index.html')

# Rota para listar todas as notas
@app.route('/notes', methods=['GET'])
def note_list():
    """
    Lista todas as notas
    ---
    tags:
      - Notas
    responses:
      200:
        description: Retorna a lista de notas
        examples:
          application/json: [{"id": 1, "title": "Exemplo", "description": "Teste"}]
    """
    notes = Note.query.all()
    return jsonify([{'id': note.id, 'title': note.title, 'description': note.description} for note in notes])

# Rota para adicionar uma nova nota
@app.route('/add_note', methods=['POST'])
def add_note():
    """
    Adiciona uma nova nota
    ---
    tags:
      - Notas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: "Nova Nota"
            description:
              type: string
              example: "Descrição da nova nota"
    responses:
      200:
        description: Nota criada com sucesso
        examples:
          application/json: {"message": "Nota criada com sucesso!"}
      400:
        description: Dados inválidos
      500:
        description: Erro ao criar nota
    """
    data = request.get_json()
    if not data or not 'title' in data or not 'description' in data:
        return jsonify({'message': 'Dados inválidos!'}), 400
    new_note = Note(title=data['title'], description=data['description'])
    try:
        db.session.add(new_note)
        db.session.commit()
        return jsonify({'message': 'Nota criada com sucesso!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao criar nota!', 'error': str(e)}), 500

# Rota para editar uma nota
@app.route('/notes/<int:id>', methods=['PUT'])
def edit_note(id):
    """
    Edita uma nota existente
    ---
    tags:
      - Notas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID da nota
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: "Nota Atualizada"
            description:
              type: string
              example: "Descrição atualizada"
    responses:
      200:
        description: Nota atualizada com sucesso
        examples:
          application/json: {"message": "Nota atualizada com sucesso!"}
      400:
        description: Dados inválidos
      404:
        description: Nota não encontrada
      500:
        description: Erro ao atualizar nota
    """
    note = Note.query.get_or_404(id)
    data = request.get_json()
    if not data or not 'title' in data or not 'description' in data:
        return jsonify({'message': 'Dados inválidos!'}), 400
    note.title = data['title']
    note.description = data['description']
    try:
        db.session.commit()
        return jsonify({'message': 'Nota atualizada com sucesso!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao atualizar nota!', 'error': str(e)}), 500

# Rota para excluir uma nota
@app.route('/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    """
    Exclui uma nota existente
    ---
    tags:
      - Notas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID da nota
    responses:
      200:
        description: Nota excluída com sucesso
        examples:
          application/json: {"message": "Nota excluída com sucesso!"}
      404:
        description: Nota não encontrada
      500:
        description: Erro ao excluir nota
    """
    note = Note.query.get_or_404(id)
    try:
        db.session.delete(note)
        db.session.commit()
        return jsonify({'message': 'Nota excluída com sucesso!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao excluir nota!', 'error': str(e)}), 500

# Rota para redirecionar para o Swagger UI
@app.route('/swagger')
def swagger_ui():
    return render_template('swagger-ui-cdn.html')

# Inicia o servidor
if __name__ == '__main__':
    app.run(debug=True)
