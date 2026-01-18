import os
from flask import Blueprint, render_template, request
from carregador import processar_index

# cria o blueprint
testes_detalhados_bp = Blueprint("testes_detalhados", __name__)

@testes_detalhados_bp.route("/teste_detalhado", methods=["GET"])
def pagina_teste_detalhado():
    """
    Página detalhada que mostra a análise de uma linha específica do CSV,
    reaproveitando a lógica de processar_index.
    """
    texto = request.args.get("linha")
    if texto:
        resposta = processar_index(texto)
    else:
        resposta = None

    id_solicitacao = request.args.get("id")
    return render_template("pagina_teste_detalhado.html", resposta=resposta, texto=texto, id=id_solicitacao)

