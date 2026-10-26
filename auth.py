from functools import wraps

from flask import jsonify, session

import models
from configdb import db


def obter_usuario_logado():
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return None

    usuario = db.session.get(models.Usuario, usuario_id)

    if not usuario or not usuario.ativo:
        session.clear()
        return None

    return usuario


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


def equipe_required(funcao):
    @wraps(funcao)
    def rota_protegida(*args, **kwargs):
        usuario = obter_usuario_logado()

        if not usuario:
            return jsonify({
                "erro": "Faça login para acessar esta página."
            }), 401

        if usuario.perfil not in ("ADMIN", "FUNCIONARIO"):
            return jsonify({
                "erro": "Acesso permitido somente à equipe."
            }), 403

        return funcao(*args, **kwargs)

    return rota_protegida