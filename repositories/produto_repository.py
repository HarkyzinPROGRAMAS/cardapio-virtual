import models
from configdb import db


def listar_todos():
    produtos = models.Product.query.order_by(
        models.Product.nome
    ).all()

    return produtos


def criar(nome, preco, disponivel, categoria="Outros"):
    produto = models.Product(
        nome=nome,
        preco=preco,
        disponivel=disponivel,
        categoria=categoria
    )

    db.session.add(produto)
    db.session.commit()

    return produto