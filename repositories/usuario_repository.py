import models
from configdb import db


def buscar_por_email(email):
    usuario = models.Usuario.query.filter_by(
        email=email
    ).first()

    return usuario


def criar_usuario(nome, email, senha, perfil):
    usuario = models.Usuario(
        nome=nome,
        email=email,
        perfil=perfil,
    )

    usuario.definir_senha(senha)

    db.session.add(usuario)
    db.session.commit()

    return usuario


def listar_todos():
    usuarios = models.Usuario.query.order_by(
        models.Usuario.nome
    ).all()

    return usuarios