from flask import Blueprint, jsonify, request, session, render_template

from services.autenticacao_service import autenticar_usuario
from auth import obter_usuario_logado

autenticacao_bp = Blueprint("autenticacao", __name__)

@autenticacao_bp.route("/login", methods=["GET"])
def pagina_login():
    return render_template("login.html")

@autenticacao_bp.route("/login", methods=["POST"])
def login():
    dados = request.get_json(silent=True) or {}

    email = str(dados.get("email", "")).strip()
    senha = str(dados.get("senha", ""))

    usuario, erro, status = autenticar_usuario(email, senha)

    if erro:
        return jsonify({"erro": erro}), status

    session.clear()
    session["usuario_id"] = usuario.id

    return jsonify({
        "mensagem": "Login realizado com sucesso.",
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "perfil": usuario.perfil
        }
    })


@autenticacao_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()

    return jsonify({
        "mensagem": "Logout realizado com sucesso."
    })


@autenticacao_bp.route("/me", methods=["GET"])
def usuario_logado():
    usuario = obter_usuario_logado()

    if not usuario:
        return jsonify({
            "erro": "Usuário não autenticado."
        }), 401

    return jsonify({
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "perfil": usuario.perfil
    })