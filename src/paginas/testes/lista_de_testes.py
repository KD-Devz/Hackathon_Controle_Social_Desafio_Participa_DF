import os

from flask import Blueprint, render_template

from src.utils.carregador import processar_testes

testes_bp = Blueprint("lista_de_testes", __name__)


@testes_bp.route("/lista_de_testes")
def pagina_testes():
    caminho_csv = os.path.join(os.path.dirname(__file__), "../../..", "testes", "AMOSTRA_e-SIC.csv")
    resposta = processar_testes(caminho_csv)

    return render_template(
        "testes/pagina_testes.html",
        cabecalho=resposta["cabecalho"],
        dados=resposta["dados"],
        total_testes=resposta["total_testes"],
        total_validos=resposta["total_validos"],
        total_invalidos=resposta["total_invalidos"]
    )
