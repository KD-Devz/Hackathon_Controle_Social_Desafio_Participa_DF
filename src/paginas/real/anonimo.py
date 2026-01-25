import sqlite3
from datetime import datetime

from flask import Blueprint, request, redirect, url_for, flash, render_template

from src.utils.banco import obter_caminho_banco
from src.utils.carregador import processar_index  # 🔹 Função de validação

# Blueprint para rotas anônimas
anonimo_bp = Blueprint("anonimo", __name__)


# 🔹 Página GET → mostra o formulário
@anonimo_bp.route("/pagina_enviar_solicitacao_anonima")
def pagina_enviar_solicitacao_anonima():
    usuario = {"nome": "Anônimo", "email": None}
    return render_template("real/pagina_enviar_solicitacao_anonima.html", usuario=usuario)


# 🔹 Rota POST → processa e salva a solicitação
@anonimo_bp.route("/enviar_solicitacao_anonima", methods=["GET", "POST"])
def enviar_solicitacao_anonima():
    texto = request.form.get("solicitacao", "").strip()
    if not texto:
        flash("A solicitação não pode estar vazia.", "error")
        return redirect(url_for("anonimo.pagina_enviar_solicitacao_anonima"))

    # Processa a mensagem com carregador.py
    resultado = processar_index(texto)

    # Se STATUS == "True" → inválida (contém dados sensíveis)
    if resultado["STATUS"] == "True":
        flash(resultado, "error")
        return redirect(url_for("anonimo.pagina_enviar_solicitacao_anonima"))

    # 🔹 Salva no banco sem vincular a um usuário
    conn = sqlite3.connect(obter_caminho_banco())
    cursor = conn.cursor()
    cursor.execute(""" INSERT INTO solicitacoes_anonimas (texto, data_envio)
                       VALUES (?, ?) """, (texto, datetime.now()))  # usuario_id = None
    conn.commit()
    conn.close()

    flash(resultado, "success")
    return redirect(url_for("anonimo.pagina_enviar_solicitacao_anonima"))
