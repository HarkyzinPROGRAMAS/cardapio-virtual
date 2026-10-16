from repositories.usuario_repository import (
    buscar_por_email,
    criar_usuario as salvar_usuario,
    listar_todos
)



def criar_usuario(dados):
    nome = str(dados.get("nome", "")).strip()
    email = str(dados.get("email", "")).strip().lower()
    senha = str(dados.get("senha", ""))
    perfil = str(
        dados.get("perfil", "FUNCIONARIO")
    ).strip().upper()

    if not nome or not email or not senha:
        return None, "Informe nome, e-mail e senha.", 400

    if len(senha) < 8:
        return None, "A senha deve ter pelo menos 8 caracteres.", 400

    if perfil not in ["ADMIN", "FUNCIONARIO"]:
        return None, "Perfil inválido.", 400

    usuario_existente = buscar_por_email(email)

    if usuario_existente:
        return None, "Já existe um usuário com este e-mail.", 400

    usuario = salvar_usuario(
        nome,
        email,
        senha,
        perfil
    )

    return usuario, None, 201


def listar_usuarios():
    return listar_todos()