import sqlite3
from datetime import datetime
from flask import Blueprint, request, redirect, url_for, flash, render_template
from src.utils.banco import obter_caminho_banco
from src.utils.carregador import processar_index

anonimo_bp = Blueprint("anonimo", __name__)

@anonimo_bp.route("/pagina_enviar_solicitacao_anonima")
def pagina_enviar_solicitacao_anonima():
    usuario = {"nome": "Anônimo", "email": None}
    return render_template("real/pagina_enviar_solicitacao_anonima.html", usuario=usuario)

@anonimo_bp.route("/enviar_solicitacao_anonima", methods=["GET", "POST"])
def enviar_solicitacao_anonima():
    texto = request.form.get("solicitacao", "").strip()
    if not texto:
        flash("A solicitação não pode estar vazia.", "error")
        return redirect(url_for("anonimo.pagina_enviar_solicitacao_anonima"))

    resultado = processar_index(texto)

    # 🔹 CORREÇÃO: Validação rigorosa e Booleanos
    tem_verbos = len(resultado.get("VERBOS", [])) > 0
    tem_interrogacoes = len(resultado.get("INTERROGACOES", [])) > 0
    status_invalido = resultado.get("STATUS") is True

    if status_invalido or tem_verbos or tem_interrogacoes:
        resultado["STATUS"] = True
        flash(resultado, "error")
        return redirect(url_for("anonimo.pagina_enviar_solicitacao_anonima"))

    conn = sqlite3.connect(obter_caminho_banco())
    cursor = conn.cursor()
    cursor.execute(""" INSERT INTO solicitacoes_anonimas (texto, data_envio)
                       VALUES (?, ?) """, (texto, datetime.now()))
    conn.commit()
    conn.close()

    flash(resultado, "success")
    return redirect(url_for("anonimo.pagina_enviar_solicitacao_anonima"))