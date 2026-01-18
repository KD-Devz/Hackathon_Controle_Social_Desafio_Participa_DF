import sqlite3
from flask import Blueprint, request, session, redirect, url_for, flash
from datetime import datetime
from src.banco import obter_caminho_banco
from src.carregador import processar_index   # 🔹 Importa a função de validação

enviar_solicitacao_bp = Blueprint("enviar_solicitacao", __name__)

@enviar_solicitacao_bp.route("/enviar_solicitacao", methods=["POST"])
def enviar_solicitacao():
    if "usuario_id" not in session:
        flash("Você precisa estar logado para enviar uma solicitação.", "error")
        return redirect(url_for("auth.login"))

    texto = request.form.get("solicitacao", "").strip()
    if not texto:
        flash("A solicitação não pode estar vazia.", "error")
        return redirect(url_for("perfil.pagina_meu_perfil"))

    # 🔹 Processa a mensagem com carregador.py
    resultado = processar_index(texto)

    # Se STATUS == "True" → inválida (contém dados sensíveis)
    if resultado["STATUS"] == "True":
        flash(resultado, "error")  # envia o resultado completo para renderizar na página
        return redirect(url_for("perfil.pagina_meu_perfil"))

    usuario_id = session["usuario_id"]

    # 🔹 Se passou na validação, salva no banco
    conn = sqlite3.connect(obter_caminho_banco())
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO solicitacoes (usuario_id, texto, data_envio)
        VALUES (?, ?, ?)
    """, (usuario_id, texto, datetime.now()))
    conn.commit()
    conn.close()

    flash(resultado, "success")  # envia o resultado completo para renderizar na página
    return redirect(url_for("perfil.pagina_meu_perfil"))
