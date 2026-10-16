from flask import Blueprint, render_template
from services.produto_service import listar_produtos

pagina_bp = Blueprint("pagina", __name__)


@pagina_bp.route("/", methods=["GET"])
def pagina_inicial():
    produtos = listar_produtos()

    return render_template(
        "index.html",
        produtos=produtos
    )