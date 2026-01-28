import sqlite3
from flask import Blueprint, request, session, redirect, url_for, flash, render_template
from datetime import datetime
from src.utils.banco import obter_caminho_banco
from src.utils.carregador import processar_index
from src.paginas.real.auth import login_required

solicitacao_bp = Blueprint("solicitacao", __name__)

@solicitacao_bp.route("/nova_solicitacao")
@login_required
def pagina_enviar_solicitacao():
    user_id = session["user_id"]
    conn = sqlite3.connect(obter_caminho_banco())
    cursor = conn.cursor()
    cursor.execute("SELECT nome, email FROM usuarios WHERE id = ?", (user_id,))
    resultado = cursor.fetchone()
    conn.close()
    usuario = {"nome": resultado[0], "email": resultado[1]} if resultado else {}
    return render_template("real/pagina_enviar_solicitacao.html", usuario=usuario)

@solicitacao_bp.route("/enviar_solicitacao", methods=["POST"])
@login_required
def enviar_solicitacao():
    texto = request.form.get("solicitacao", "").strip()
    if not texto:
        flash("A solicitação não pode estar vazia.", "error")
        return redirect(url_for("solicitacao.pagina_enviar_solicitacao"))

    # Processa a análise
    resultado = processar_index(texto)

    # 🔹 CORREÇÃO: Lógica rigorosa e uso de booleanos reais (sem aspas)
    # Se status for True OU houver itens nas listas de verbos/interrogações -> Inválido
    tem_verbos = len(resultado.get("VERBOS", [])) > 0
    tem_interrogacoes = len(resultado.get("INTERROGACOES", [])) > 0
    status_invalido = resultado.get("STATUS") is True

    if status_invalido or tem_verbos or tem_interrogacoes:
        # Garante que o status no dicionário de retorno seja consistente para o HTML
        resultado["STATUS"] = True
        flash(resultado, "error")
        return redirect(url_for("solicitacao.pagina_enviar_solicitacao"))

    user_id = session["user_id"]
    conn = sqlite3.connect(obter_caminho_banco())
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO solicitacoes (usuario_id, texto, data_envio)
        VALUES (?, ?, ?)
    """, (user_id, texto, datetime.now()))
    conn.commit()
    conn.close()

    flash(resultado, "success")
    return redirect(url_for("solicitacao.pagina_enviar_solicitacao"))

@solicitacao_bp.route("/ver_solicitacoes")
@login_required
def ver_solicitacoes():
    user_id = session["user_id"]
    conn = sqlite3.connect(obter_caminho_banco())
    cursor = conn.cursor()
    cursor.execute("""
        SELECT texto, data_envio, id 
        FROM solicitacoes 
        WHERE usuario_id = ? 
        ORDER BY data_envio DESC
    """, (user_id,))
    solicitacoes = cursor.fetchall()
    conn.close()
    return render_template("real/pagina_ver_solicitacoes.html", solicitacoes=solicitacoes)

@solicitacao_bp.route("/detalhes_solicitacao/<int:solicitacao_id>")
@login_required
def detalhes_solicitacao(solicitacao_id):
    conn = sqlite3.connect(obter_caminho_banco())
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT texto, data_envio
                   FROM solicitacoes
                   WHERE id = ? AND usuario_id = ?
                   """, (solicitacao_id, session["user_id"]))
    resultado_db = cursor.fetchone()
    conn.close()

    if not resultado_db:
        flash("Solicitação não encontrada.", "error")
        return redirect(url_for("solicitacao.ver_solicitacoes"))

    texto_solicitacao = resultado_db[0]
    analise = processar_index(texto_solicitacao)

    return render_template(
        "real/pagina_detalhes_analise.html",
        id=solicitacao_id,
        texto=texto_solicitacao,
        resposta=analise
    )