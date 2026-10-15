import os
from flask import Flask, jsonify, request, session
from decimal import Decimal, InvalidOperation
from flask_migrate import Migrate
from dotenv import load_dotenv
from configdb import db
import models

load_dotenv()

app = Flask(__name__)
from functools import wraps
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db.init_app(app)
migrate = Migrate(app,db)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

if not app.config["SECRET_KEY"]:
    raise RuntimeError("SECRET_KEY não foi definida no arquivo .env")

def obter_usuario_logado():
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return None

    usuario = db.session.get(models.Usuario, usuario_id)

    if not usuario or not usuario.ativo:
        session.clear()
        return None

    return usuario


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


def admin_required(funcao):
    @wraps(funcao)
    def rota_protegida(*args, **kwargs):
        usuario = obter_usuario_logado()

        if not usuario:
            return jsonify({
                "erro": "Faça login para acessar esta rota."
            }), 401

        if usuario.perfil != "ADMIN":
            return jsonify({
                "erro": "Acesso permitido somente para administradores."
            }), 403

        return funcao(*args, **kwargs)

    return rota_protegida

@app.route("/usuarios", methods=["POST"])
@admin_required
def criar_usuario():
    dados = request.get_json(silent=True) or {}

    nome = str(dados.get("nome", "")).strip()
    email = str(dados.get("email", "")).strip().lower()
    senha = str(dados.get("senha", ""))
    perfil = str(dados.get("perfil", "FUNCIONARIO")).strip().upper()

    if not nome or not email or not senha:
        return jsonify({
            "erro": "Informe nome, e-mail e senha."
        }), 400

    if len(senha) < 8:
        return jsonify({
            "erro": "A senha deve ter pelo menos 8 caracteres."
        }), 400

    if perfil not in ["ADMIN", "FUNCIONARIO"]:
        return jsonify({
            "erro": "Perfil inválido."
        }), 400

    usuario_existente = models.Usuario.query.filter_by(
        email=email
    ).first()

    if usuario_existente:
        return jsonify({
            "erro": "Já existe um usuário com este e-mail."
        }), 400

    usuario = models.Usuario(
        nome=nome,
        email=email,
        perfil=perfil,
    )

    usuario.definir_senha(senha)

    db.session.add(usuario)
    db.session.commit()

    return jsonify({
        "mensagem": "Usuário criado com sucesso.",
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "perfil": usuario.perfil,
            "ativo": usuario.ativo,
        }
    }), 201

@app.route("/login", methods=["POST"])
def login():
    dados = request.get_json(silent=True) or {}

    email = str(dados.get("email", "")).strip()
    senha = str(dados.get("senha", ""))

    if not email or not senha:
        return jsonify({
            "erro": "Informe e-mail e senha."
        }), 400

    usuario = models.Usuario.query.filter_by(email=email).first()

    if not usuario or not usuario.verificar_senha(senha):
        return jsonify({
            "erro": "E-mail ou senha inválidos."
        }), 401

    if not usuario.ativo:
        return jsonify({
            "erro": "Este usuário está desativado."
        }), 403

    session.clear()
    session["usuario_id"] = usuario.id

    return jsonify({
        "mensagem": "Login realizado com sucesso.",
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "perfil": usuario.perfil,
        }
    })


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()

    return jsonify({
        "mensagem": "Logout realizado com sucesso."
    })


@app.route("/me", methods=["GET"])
def usuario_logado():
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return jsonify({
            "erro": "Usuário não autenticado."
        }), 401

    usuario = db.session.get(models.Usuario, usuario_id)

    if not usuario or not usuario.ativo:
        session.clear()

        return jsonify({
            "erro": "Usuário não autenticado."
        }), 401

    return jsonify({
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "perfil": usuario.perfil,
    })

@app.route("/usuarios", methods=["GET"])
@admin_required
def listar_usuarios():
    usuarios = models.Usuario.query.order_by(
        models.Usuario.nome
    ).all()

    return jsonify([
        {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "perfil": usuario.perfil,
            "ativo": usuario.ativo,
            "criado_em": usuario.criado_em.isoformat(),
        }
        for usuario in usuarios
    ])

@app.route("/produtos", methods=["GET"])
def listar_produtos():
    produtos = models.Product.query.order_by(models.Product.nome).all()

    return jsonify([
        {
            "id": produto.id,
            "nome": produto.nome,
            "preco": str(produto.preco),
            "disponivel": produto.disponivel,
        }
        for produto in produtos
    ])


@app.route("/produtos", methods=["POST"])
def criar_produto():
    dados = request.get_json(silent=True) or {}

    nome = str(dados.get("nome", "")).strip()
    preco_recebido = dados.get("preco")
    disponivel = dados.get("disponivel", True)

    if not nome or preco_recebido is None:
        return jsonify({
            "erro": "Informe nome e preço do produto."
        }), 400

    try:
        preco = Decimal(str(preco_recebido))
    except (InvalidOperation, ValueError):
        return jsonify({
            "erro": "O preço informado é inválido."
        }), 400

    if preco < 0:
        return jsonify({
            "erro": "O preço não pode ser negativo."
        }), 400

    produto = models.Product(
        nome=nome,
        preco=preco,
        disponivel=disponivel,
    )

    db.session.add(produto)
    db.session.commit()

    return jsonify({
        "mensagem": "Produto criado com sucesso.",
        "produto": {
            "id": produto.id,
            "nome": produto.nome,
            "preco": str(produto.preco),
            "disponivel": produto.disponivel,
        }
    }), 201

@app.route("/pedidos", methods=["POST"])
def criar_pedido():
    dados = request.get_json(silent=True) or {}

    try:
        numero_mesa = int(dados.get("numero_mesa"))
    except (TypeError, ValueError):
        return jsonify({
            "erro": "Informe um número de mesa válido."
        }), 400

    nome_cliente = str(dados.get("nome_cliente", "")).strip()
    telefone_cliente = str(dados.get("telefone_cliente", "")).strip() or None
    itens_recebidos = dados.get("itens", [])

    if numero_mesa <= 0:
        return jsonify({
            "erro": "O número da mesa deve ser maior que zero."
        }), 400

    if not nome_cliente:
        return jsonify({
            "erro": "Informe o nome do cliente."
        }), 400

    if not isinstance(itens_recebidos, list) or not itens_recebidos:
        return jsonify({
            "erro": "Adicione pelo menos um item ao pedido."
        }), 400

    itens_validos = []
    total = Decimal("0.00")

    for item in itens_recebidos:
        try:
            produto_id = int(item.get("produto_id"))
            quantidade = int(item.get("quantidade", 1))
        except (TypeError, ValueError):
            return jsonify({
                "erro": "Produto ou quantidade inválidos."
            }), 400

        if quantidade <= 0:
            return jsonify({
                "erro": "A quantidade deve ser maior que zero."
            }), 400

        produto = db.session.get(models.Product, produto_id)

        if not produto:
            return jsonify({
                "erro": f"Produto com ID {produto_id} não encontrado."
            }), 404

        if not produto.disponivel:
            return jsonify({
                "erro": f"O produto {produto.nome} não está disponível."
            }), 400

        itens_validos.append({
            "produto": produto,
            "quantidade": quantidade,
        })

        total += produto.preco * quantidade

    pedido = models.Pedido(
        numero_mesa=numero_mesa,
        nome_cliente=nome_cliente,
        telefone_cliente=telefone_cliente,
        total=total,
    )

    for item in itens_validos:
        produto = item["produto"]

        pedido.itens.append(models.ItemPedido(
            produto_id=produto.id,
            quantidade=item["quantidade"],
            preco_unitario=produto.preco,
        ))

    db.session.add(pedido)
    db.session.commit()

    return jsonify({
        "mensagem": "Pedido criado com sucesso.",
        "pedido": {
            "id": pedido.id,
            "mesa": pedido.numero_mesa,
            "cliente": pedido.nome_cliente,
            "status": pedido.status,
            "total": str(pedido.total),
        }
    }), 201

@app.route("/pedidos", methods=["GET"])
def listar_pedidos():
    status = request.args.get("status", "").strip()

    consulta = models.Pedido.query

    if status:
        consulta = consulta.filter_by(status=status)

    pedidos = consulta.order_by(
        models.Pedido.criado_em.desc()
    ).all()

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

    return jsonify(resultado)

@app.route("/pedidos/<int:pedido_id>/status", methods=["PATCH"])
def atualizar_status_pedido(pedido_id):
    dados = request.get_json(silent=True) or {}
    novo_status = str(dados.get("status", "")).strip()

    status_permitidos = [
        "Pendente",
        "Em preparo",
        "Pronto",
        "Finalizado",
        "Cancelado",
    ]

    if novo_status not in status_permitidos:
        return jsonify({
            "erro": "Status inválido.",
            "status_permitidos": status_permitidos,
        }), 400

    pedido = db.session.get(models.Pedido, pedido_id)

    if not pedido:
        return jsonify({
            "erro": "Pedido não encontrado."
        }), 404

    pedido.status = novo_status
    db.session.commit()

    return jsonify({
        "mensagem": "Status atualizado com sucesso.",
        "pedido": {
            "id": pedido.id,
            "mesa": pedido.numero_mesa,
            "status": pedido.status,
        }
    })

@app.route("/pedidos/<int:pedido_id>/pagamento", methods=["POST"])
def registrar_pagamento(pedido_id):
    dados = request.get_json(silent=True) or {}
    metodo = str(dados.get("metodo", "")).strip()

    metodos_permitidos = ["Pix", "Dinheiro", "Cartão"]

    if metodo not in metodos_permitidos:
        return jsonify({
            "erro": "Método de pagamento inválido.",
            "metodos_permitidos": metodos_permitidos,
        }), 400

    pedido = db.session.get(models.Pedido, pedido_id)

    if not pedido:
        return jsonify({
            "erro": "Pedido não encontrado."
        }), 404

    if pedido.pagamento:
        return jsonify({
            "erro": "Este pedido já possui um pagamento registrado."
        }), 400

    pagamento = models.Pagamento(
        pedido_id=pedido.id,
        metodo=metodo,
        valor=pedido.total,
    )

    db.session.add(pagamento)
    db.session.commit()

    return jsonify({
        "mensagem": "Pagamento registrado com sucesso.",
        "pagamento": {
            "id": pagamento.id,
            "pedido_id": pedido.id,
            "metodo": pagamento.metodo,
            "valor": str(pagamento.valor),
            "pago_em": pagamento.pago_em.isoformat(),
        }
    }), 201


    
from sqlalchemy import text

with app.app_context():
    resultado = db.session.execute(text("SELECT 1"))
    print("Conexao OK:", resultado.scalar())