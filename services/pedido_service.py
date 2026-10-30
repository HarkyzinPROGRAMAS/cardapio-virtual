from decimal import Decimal

from repositories.pedido_repository import (
    listar_pedidos as buscar_pedidos,
    buscar_produto_por_id,
    criar_pedido as salvar_pedido,
    buscar_pedido_por_id,
    atualizar_status as salvar_status,
    registrar_pagamento as salvar_pagamento,
    arquivar_pedido as salvar_arquivamento
)


def listar_pedidos(status=""):
    pedidos = buscar_pedidos(status)

    resultado = []

    for pedido in pedidos:
        itens = []

        for item in pedido.itens:
            itens.append({
                "produto": item.produto.nome,
                "quantidade": item.quantidade,
                "preco_unitario": str(item.preco_unitario),
            })

        pagamento = None

        if pedido.pagamento:
            pagamento = {
                "metodo": pedido.pagamento.metodo,
                "valor": str(pedido.pagamento.valor),
                "pago_em": pedido.pagamento.pago_em.isoformat(),
            }

        resultado.append({
            "id": pedido.id,
            "mesa": pedido.numero_mesa,
            "cliente": pedido.nome_cliente,
            "telefone": pedido.telefone_cliente,
            "status": pedido.status,
            "total": str(pedido.total),
            "criado_em": pedido.criado_em.isoformat(),
            "itens": itens,
            "pagamento": pagamento,
        })

    return resultado


def criar_pedido(dados):
    try:
        numero_mesa = int(dados.get("numero_mesa"))
    except (TypeError, ValueError):
        return None, "Informe um número de mesa válido.", 400

    nome_cliente = str(
        dados.get("nome_cliente", "")
    ).strip()

    telefone_cliente = str(
        dados.get("telefone_cliente", "")
    ).strip() or None

    itens_recebidos = dados.get("itens", [])

    if numero_mesa <= 0:
        return None, "O número da mesa deve ser maior que zero.", 400

    if not nome_cliente:
        return None, "Informe o nome do cliente.", 400

    if not isinstance(itens_recebidos, list) or not itens_recebidos:
        return None, "Adicione pelo menos um item ao pedido.", 400

    itens_validos = []
    total = Decimal("0.00")

    for item in itens_recebidos:
        if not isinstance(item, dict):
            return None, "Produto ou quantidade inválidos.", 400

        try:
            produto_id = int(item.get("produto_id"))
            quantidade = int(item.get("quantidade", 1))
        except (TypeError, ValueError):
            return None, "Produto ou quantidade inválidos.", 400

        if quantidade <= 0:
            return None, "A quantidade deve ser maior que zero.", 400

        produto = buscar_produto_por_id(produto_id)

        if not produto:
            return None, f"Produto com ID {produto_id} não encontrado.", 404

        if not produto.disponivel:
            return None, f"O produto {produto.nome} não está disponível.", 400

        itens_validos.append({
            "produto": produto,
            "quantidade": quantidade,
        })

        total += produto.preco * quantidade

    pedido = salvar_pedido(
        numero_mesa,
        nome_cliente,
        telefone_cliente,
        itens_validos,
        total
    )

    return pedido, None, 201

def atualizar_status_pedido(pedido_id, novo_status):
    status_permitidos = [
        "Pendente",
        "Em preparo",
        "Pronto",
        "Finalizado",
        "Cancelado",
    ]

    if novo_status not in status_permitidos:
        return None, "Status inválido.", 400

    pedido = buscar_pedido_por_id(pedido_id)

    if not pedido:
        return None, "Pedido não encontrado.", 404

    if pedido.arquivado:
        return None, "Este pedido já foi retirado do painel.", 400

    transicoes_permitidas = {
        "Pendente": ["Em preparo", "Cancelado"],
        "Em preparo": ["Pronto", "Cancelado"],
        "Pronto": ["Finalizado"],
        "Finalizado": [],
        "Cancelado": [],
    }

    if novo_status not in transicoes_permitidas[pedido.status]:
        return None, "Não é permitido realizar essa mudança de status.", 400

    pedido = salvar_status(pedido, novo_status)

    return pedido, None, 200


def registrar_pagamento(pedido_id, metodo):
    metodos_permitidos = ["Pix", "Dinheiro", "Cartão"]

    if metodo not in metodos_permitidos:
        return None, "Método de pagamento inválido.", 400

    pedido = buscar_pedido_por_id(pedido_id)

    if not pedido:
        return None, "Pedido não encontrado.", 404

    if pedido.arquivado:
        return None, "Este pedido já foi retirado do painel.", 400

    if pedido.status == "Cancelado":
        return None, "Não é possível registrar pagamento para um pedido cancelado.", 400

    if pedido.pagamento:
        return None, "Este pedido já possui um pagamento registrado.", 400

    pagamento = salvar_pagamento(pedido, metodo)

    return pagamento, None, 201


def arquivar_pedido(pedido_id):
    pedido = buscar_pedido_por_id(pedido_id)

    if not pedido:
        return None, "Pedido não encontrado.", 404

    if pedido.arquivado:
        return None, "Este pedido já foi retirado do painel.", 400

    if pedido.status != "Finalizado":
        return None, "Somente pedidos finalizados podem ser arquivados.", 400

    if not pedido.pagamento:
        return None, "O pagamento precisa estar registrado para arquivar o pedido.", 400

    pedido = salvar_arquivamento(pedido)

    return pedido, None, 200