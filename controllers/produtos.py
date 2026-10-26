from flask import Blueprint, jsonify, request

from services.produto_service import (
    listar_produtos,
    criar_produto as criar_produto_service
)

produtos_bp = Blueprint("produtos", __name__)


@produtos_bp.route("/produtos", methods=["GET"])
def listar_produtos_controller():
    produtos = listar_produtos()

    return jsonify([
        {
            "id": produto.id,
            "nome": produto.nome,
            "preco": str(produto.preco),
            "disponivel": produto.disponivel,
        }
        for produto in produtos
    ])


@produtos_bp.route("/produtos", methods=["POST"])
def criar_produto_controller():
    dados = request.get_json(silent=True) or {}

    produto, erro = criar_produto_service(dados)

    if erro:
        return jsonify({"erro": erro}), 400

    return jsonify({
        "mensagem": "Produto criado com sucesso.",
        "produto": {
            "id": produto.id,
            "nome": produto.nome,
            "preco": str(produto.preco),
            "disponivel": produto.disponivel,
        }
    }), 201
