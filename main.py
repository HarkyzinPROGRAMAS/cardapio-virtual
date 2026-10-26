import os
from controllers.produtos import produtos_bp
from controllers.pedidos import pedidos_bp
from controllers.usuarios import usuarios_bp
from controllers.autenticacao import autenticacao_bp
from controllers.pagina import pagina_bp
from flask import Flask, jsonify, request, session
from decimal import Decimal, InvalidOperation
from flask_migrate import Migrate
from dotenv import load_dotenv
from configdb import db
from auth import obter_usuario_logado, admin_required
import models

load_dotenv()

app = Flask(__name__)
from functools import wraps
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db.init_app(app)
migrate = Migrate(app,db)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.register_blueprint(produtos_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(autenticacao_bp)
app.register_blueprint(pagina_bp)
if not app.config["SECRET_KEY"]:
    raise RuntimeError("SECRET_KEY não foi definida no arquivo .env")

def login_required(funcao):
    @wraps(funcao)
    def rota_protegida(*args, **kwargs):
        usuario = obter_usuario_logado()

        if not usuario:
            return jsonify({
                "erro": "Faça login para acessar esta rota."
            }), 401

        return funcao(*args, **kwargs)

    return rota_protegida
    
from sqlalchemy import text

with app.app_context():
    resultado = db.session.execute(text("SELECT 1"))
    print("Conexao OK:", resultado.scalar())