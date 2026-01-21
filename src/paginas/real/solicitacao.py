import sqlite3
from flask import Blueprint, request, session, redirect, url_for, flash, render_template
from datetime import datetime
from src.utils.banco import obter_caminho_banco
from src.utils.carregador import processar_index   # 🔹 Função de validação
from src.paginas.real.auth import login_required

solicitacao_bp = Blueprint("solicitacao", __name__)

# 🔹 Rota GET → abre a página com o formulário
@solicitacao_bp.route("/nova_solicitacao")
@login_required
def pagina_enviar_solicitacao():
    user_id = session["user_id"]

    # Busca dados do usuário para exibir na página
    conn = sqlite3.connect(obter_caminho_banco())
    cursor = conn.cursor()
    cursor.execute("SELECT nome, email FROM usuarios WHERE id = ?", (user_id,))
    resultado = cursor.fetchone()
    conn.close()

    usuario = {"nome": resultado[0], "email": resultado[1]} if resultado else {}

    return render_template("real/pagina_enviar_solicitacao.html", usuario=usuario)


# 🔹 Rota POST → processa e salva a solicitação
@solicitacao_bp.route("/enviar_solicitacao", methods=["POST"])
@login_required
def enviar_solicitacao():
    texto = request.form.get("solicitacao", "").strip()
    if not texto:
        flash("A solicitação não pode estar vazia.", "error")
        return redirect(url_for("solicitacao.pagina_enviar_solicitacao"))

    # 🔹 Processa a mensagem com carregador.py
    resultado = processar_index(texto)

    # Se STATUS == "True" → inválida (contém dados sensíveis)
    if resultado["STATUS"] == "True":
        flash(resultado, "error")  # envia o resultado completo para renderizar na página
        return redirect(url_for("solicitacao.pagina_enviar_solicitacao"))

    user_id = session["user_id"]

    # 🔹 Se passou na validação, salva no banco
    conn = sqlite3.connect(obter_caminho_banco())
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO solicitacoes (usuario_id, texto, data_envio)
        VALUES (?, ?, ?)
    """, (user_id, texto, datetime.now()))
    conn.commit()
    conn.close()

    flash(resultado, "success")  # envia o resultado completo para renderizar na página
    return redirect(url_for("solicitacao.pagina_enviar_solicitacao"))


# 🔹 Rota GET → ver histórico de solicitações
@solicitacao_bp.route("/ver_solicitacoes")
@login_required
def ver_solicitacoes():
    user_id = session["user_id"]

    conn = sqlite3.connect(obter_caminho_banco())
    cursor = conn.cursor()
    cursor.execute("""
        SELECT texto, data_envio
        FROM solicitacoes
        WHERE usuario_id = ?
        ORDER BY data_envio DESC
    """, (user_id,))
    solicitacoes = cursor.fetchall()
    conn.close()

    return render_template("real/pagina_ver_solicitacoes.html", solicitacoes=solicitacoes)
