from decimal import Decimal, InvalidOperation

from repositories.produto_repository import (
    listar_todos,
    criar as criar_produto_no_banco
)


def listar_produtos():
    return listar_todos()


def criar_produto(dados):
    nome = str(dados.get("nome", "")).strip()
    preco_recebido = dados.get("preco")
    disponivel = dados.get("disponivel", True)
    categoria = str(dados.get("categoria", "Outros")).strip()

    categorias_validas = [
    "Cafe",
    "Bebidas",
    "Salgados",
    "Doces",
    "Extras",
    "Lanches",
    "Outros"
    ]

    if categoria not in categorias_validas:
        return None, "Categoria inválida."

    if not nome or preco_recebido is None:
        return None, "Informe nome e preço do produto."

    try:
        preco = Decimal(str(preco_recebido))
    except (InvalidOperation, ValueError):
        return None, "O preço informado é inválido."

    if preco < 0:
        return None, "O preço não pode ser negativo."

    produto = criar_produto_no_banco(
        nome,
        preco,
        disponivel,
        categoria
    )

    return produto, None