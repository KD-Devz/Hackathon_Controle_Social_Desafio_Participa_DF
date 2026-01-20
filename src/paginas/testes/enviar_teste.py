from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages
from src.utils.carregador import processar_index
enviar_bp = Blueprint("enviar_testes", __name__)

@enviar_bp.route("/enviar_testes", methods=["GET", "POST"])
def pagina_enviar_teste():
    if request.method == "POST":
        mensagem = request.form.get("menssagem")
        if mensagem:
            resposta = processar_index(mensagem)
            flash(resposta)
            return redirect(url_for("enviar_testes.pagina_enviar_teste"))

    mensagens = get_flashed_messages()
    resposta = mensagens[0] if mensagens else None
    return render_template("testes/pagina_enviar_teste.html", resposta=resposta)