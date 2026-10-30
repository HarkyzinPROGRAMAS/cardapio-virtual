
import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate

from configdb import db
import models

from controllers.produtos import produtos_bp
from controllers.pedidos import pedidos_bp
from controllers.usuarios import usuarios_bp
from controllers.autenticacao import autenticacao_bp
from controllers.pagina import pagina_bp


load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

if not app.config["SECRET_KEY"]:
    raise RuntimeError("SECRET_KEY não foi definida no arquivo .env")

db.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(produtos_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(autenticacao_bp)
app.register_blueprint(pagina_bp)
