from flask import Blueprint, jsonify, request
from services.usuario_service import (
    criar_usuario,
    listar_usuarios as listar_usuarios_service
)
from auth import admin_required

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/usuarios", methods=["POST"])
@admin_required
def criar_usuario_controller():
    dados = request.get_json(silent=True) or {}

    usuario, erro, status = criar_usuario(dados)

    if erro:
        return jsonify({"erro": erro}), status

    return jsonify({
        "mensagem": "Usuário criado com sucesso.",
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "perfil": usuario.perfil,
            "ativo": usuario.ativo
        }
    }), status


@usuarios_bp.route("/usuarios", methods=["GET"])
@admin_required
def listar_usuarios_controller():
    usuarios = listar_usuarios_service()

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