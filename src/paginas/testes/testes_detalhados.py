from flask import Blueprint, render_template, request
from src.utils.carregador import processar_index

testes_detalhados_bp = Blueprint("testes_detalhados", __name__)
@testes_detalhados_bp.route("/teste_detalhado", methods=["GET"])
def pagina_teste_detalhado():
    texto = request.args.get("linha")
    if texto:
        resposta = processar_index(texto)
    else:
        resposta = None

    id_solicitacao = request.args.get("id")
    return render_template("testes/pagina_teste_detalhado.html", resposta=resposta, texto=texto, id=id_solicitacao)
