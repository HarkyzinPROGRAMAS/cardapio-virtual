import models
from configdb import db

def listar_pedidos(status="", incluir_arquivados=False):
    consulta = models.Pedido.query

    if not incluir_arquivados:
        consulta = consulta.filter_by(arquivado=False)

    if status:
        consulta = consulta.filter_by(status=status)

    pedidos = consulta.order_by(
        models.Pedido.criado_em.desc()
    ).all()

    return pedidos


def buscar_produto_por_id(produto_id):
    produto = db.session.get(
        models.Product,
        produto_id
    )

    return produto


def criar_pedido(
    numero_mesa,
    nome_cliente,
    telefone_cliente,
    itens_validos,
    total
):
    pedido = models.Pedido(
        numero_mesa=numero_mesa,
        nome_cliente=nome_cliente,
        telefone_cliente=telefone_cliente,
        total=total
    )

    for item in itens_validos:
        produto = item["produto"]

        pedido.itens.append(models.ItemPedido(
            produto_id=produto.id,
            quantidade=item["quantidade"],
            preco_unitario=produto.preco
        ))

    db.session.add(pedido)
    db.session.commit()

    return pedido


def buscar_pedido_por_id(pedido_id):
    pedido = db.session.get(
        models.Pedido,
        pedido_id
    )

    return pedido


def atualizar_status(pedido, novo_status):
    pedido.status = novo_status

    db.session.commit()

    return pedido


def registrar_pagamento(pedido, metodo):
    pagamento = models.Pagamento(
        pedido_id=pedido.id,
        metodo=metodo,
        valor=pedido.total
    )

    db.session.add(pagamento)
    db.session.commit()

    return pagamento

def arquivar_pedido(pedido):
    pedido.arquivado = True

    db.session.commit()

    return pedido