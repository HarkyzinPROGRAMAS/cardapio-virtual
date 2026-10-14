import os
from flask import Flask
from dotenv import load_dotenv
from configdb import db

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db.init_app(app)

from sqlalchemy import text

with app.app_context():
    resultado = db.session.execute(text("SELECT 1"))
    print("Conexao OK:", resultado.scalar())