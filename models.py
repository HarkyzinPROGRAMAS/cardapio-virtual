from datetime import datetime

from configdb import db

from werkzeug.security import generate_password_hash, check_password_hash

class Product(db.Model):
    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    disponivel = db.Column(db.Boolean, default=True)

    categoria = db.Column(
        db.String(50),
        nullable=False,
        default="Outros",
        server_default="Outros"
    )

class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)

    numero_mesa = db.Column(db.Integer, nullable=False)
    nome_cliente = db.Column(db.String(100), nullable=False)
    telefone_cliente = db.Column(db.String(20), nullable=True)

    status = db.Column(db.String(30), default="Pendente")

    arquivado = db.Column(
    db.Boolean,
    nullable=False,
    default=False,
    server_default=db.false()
    )

    total = db.Column(db.Numeric(10, 2), default=0)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    itens = db.relationship("ItemPedido", backref="pedido", lazy=True)
    pagamento = db.relationship("Pagamento",backref="pedido",uselist=False)

class ItemPedido(db.Model):
    __tablename__ = "itens_pedido"

    id = db.Column(db.Integer, primary_key=True)

    pedido_id = db.Column(db.Integer,db.ForeignKey("pedidos.id"),nullable=False,)
    produto_id = db.Column(db.Integer,db.ForeignKey("produtos.id"),nullable=False)

    quantidade = db.Column(db.Integer, default=1)

    preco_unitario = db.Column(db.Numeric(10, 2), nullable=False)

    produto = db.relationship("Product")


class Pagamento(db.Model):
    __tablename__ = "pagamentos"

    id = db.Column(db.Integer, primary_key=True)

    pedido_id = db.Column(db.Integer,db.ForeignKey("pedidos.id"),nullable=False,unique=True)


    metodo = db.Column(db.String(20), nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    pago_em = db.Column(db.DateTime, default=datetime.utcnow)


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)

    
    senha_hash = db.Column(db.String(255), nullable=False)

    
    perfil = db.Column(db.String(20), nullable=False, default="FUNCIONARIO")

    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def definir_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)