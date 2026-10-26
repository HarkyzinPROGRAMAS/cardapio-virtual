from repositories.usuario_repository import buscar_por_email


def autenticar_usuario(email, senha):
    if not email or not senha:
        return None, "Informe e-mail e senha.", 400

    usuario = buscar_por_email(email)

    if not usuario or not usuario.verificar_senha(senha):
        return None, "E-mail ou senha inválidos.", 401

    if not usuario.ativo:
        return None, "Este usuário está desativado.", 403

    return usuario, None, 200