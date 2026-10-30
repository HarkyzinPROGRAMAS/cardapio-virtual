import base64
import io
import qrcode

from flask import Blueprint, jsonify, request, render_template

from services.pedido_service import (
    listar_pedidos as buscar_pedidos,
    criar_pedido as criar_pedido_service,
    atualizar_status_pedido as atualizar_status_service,
    registrar_pagamento as registrar_pagamento_service,
    arquivar_pedido as arquivar_pedido_service
)

from auth import equipe_required

pedidos_bp = Blueprint("pedidos", __name__)
@pedidos_bp.route("/painel-pedidos", methods=["GET"])
@equipe_required
def painel_pedidos():
    return render_template("pedidos.html")

@pedidos_bp.route("/qr-codes", methods=["GET"])
@equipe_required
def pagina_qr_codes():
    mesas = []
    base_url = request.host_url.rstrip("/")

    for numero in range(1, 11):
        url_cardapio = f"{base_url}/?mesa={numero}"

        imagem = qrcode.make(url_cardapio)

        buffer = io.BytesIO()
        imagem.save(buffer, format="PNG")

        imagem_base64 = base64.b64encode(
            buffer.getvalue()
        ).decode("utf-8")

        mesas.append({
            "numero": numero,
            "url": url_cardapio,
            "imagem": imagem_base64
        })

    return render_template("qr_codes.html", mesas=mesas)

@pedidos_bp.route("/pedidos", methods=["GET"])
@equipe_required
def listar_pedidos_controller():
    status = request.args.get("status", "").strip()

    resultado = buscar_pedidos(status)

    return jsonify(resultado)


@pedidos_bp.route("/pedidos", methods=["POST"])
def criar_pedido_controller():
    dados = request.get_json(silent=True) or {}

    pedido, erro, status_http = criar_pedido_service(dados)

    if erro:
        return jsonify({"erro": erro}), status_http

    return jsonify({
        "mensagem": "Pedido criado com sucesso.",
        "pedido": {
            "id": pedido.id,
            "mesa": pedido.numero_mesa,
            "cliente": pedido.nome_cliente,
            "status": pedido.status,
            "total": str(pedido.total),
        }
    }), status_http


@pedidos_bp.route(
    "/pedidos/<int:pedido_id>/status",
    methods=["PATCH"]
)
@equipe_required
def atualizar_status_controller(pedido_id):
    dados = request.get_json(silent=True) or {}
    novo_status = str(dados.get("status", "")).strip()

    pedido, erro, status_http = atualizar_status_service(
        pedido_id,
        novo_status
    )

    if erro:
        return jsonify({"erro": erro}), status_http

    return jsonify({
        "mensagem": "Status atualizado com sucesso.",
        "pedido": {
            "id": pedido.id,
            "mesa": pedido.numero_mesa,
            "status": pedido.status,
        }
    }), status_http


@pedidos_bp.route(
    "/pedidos/<int:pedido_id>/pagamento",
    methods=["POST"]
)
@equipe_required
def registrar_pagamento_controller(pedido_id):
    dados = request.get_json(silent=True) or {}
    metodo = str(dados.get("metodo", "")).strip()

    pagamento, erro, status_http = registrar_pagamento_service(
        pedido_id,
        metodo
    )

    if erro:
        return jsonify({"erro": erro}), status_http

    return jsonify({
        "mensagem": "Pagamento registrado com sucesso.",
        "pagamento": {
            "id": pagamento.id,
            "pedido_id": pagamento.pedido_id,
            "metodo": pagamento.metodo,
            "valor": str(pagamento.valor),
            "pago_em": pagamento.pago_em.isoformat(),
        }
    }), status_http


@pedidos_bp.route(
    "/pedidos/<int:pedido_id>/arquivar",
    methods=["PATCH"]
)
@equipe_required
def arquivar_pedido_controller(pedido_id):
    pedido, erro, status_http = arquivar_pedido_service(pedido_id)

    if erro:
        return jsonify({"erro": erro}), status_http

    return jsonify({
        "mensagem": "Pedido retirado do painel com sucesso.",
        "pedido": {
            "id": pedido.id,
            "status": pedido.status,
            "arquivado": pedido.arquivado
        }
    }), status_http