from flask import Flask, jsonify
from celery import Celery
from flaskCelery import make_celery
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teste.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Produtos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_nome = db.Column(db.String, nullable=False)

app.config.update(
    CELERY_BROKER_URL = 'redis://localhost:6379/0',
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
)
celery = make_celery(app)

@celery.task(name='function_cadastro')
def cadastrador_assincrono(produto):
    adicionar = Produtos(produto_nome=produto)
    db.session.add(adicionar)
    db.session.commit()
    return True

@app.route('/cadastro/<produto>', methods=['GET', 'POST'])
def cadastro_produto(produto):
    cadastrador_assincrono.delay(produto)
    return "Cadastrando Produto..."

if __name__ == '__main__':
    app.run(debug=True)