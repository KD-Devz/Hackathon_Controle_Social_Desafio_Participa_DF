from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages
from carregador import processar_index

index_bp = Blueprint("index", __name__)

@index_bp.route("/", methods=["GET", "POST"])
def pagina_index():
    if request.method == "POST":
        mensagem = request.form.get("menssagem")
        if mensagem:
            resposta = processar_index(mensagem)
            flash(resposta)
            return redirect(url_for("index.pagina_index"))

    mensagens = get_flashed_messages()
    resposta = mensagens[0] if mensagens else None
    return render_template("pagina_index.html", resposta=resposta)
