import os
import sqlite3

from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask import request  # Adicione ao topo do arquivo

from src.paginas.real.auth import login_required
from src.utils.banco import obter_caminho_banco

perfil_bp = Blueprint("perfil", __name__)


@perfil_bp.route("/meu_perfil")
@login_required
def pagina_meu_perfil():
    user_id = session["user_id"]
    conn = sqlite3.connect(obter_caminho_banco())
    cursor = conn.cursor()

    # 🔹 Adicione 'foto' e as outras colunas aqui!
    cursor.execute("SELECT nome, email, bio, telefone, github, foto FROM usuarios WHERE id = ?", (user_id,))
    res = cursor.fetchone()
    conn.close()

    usuario = {
        "nome": res[0],
        "email": res[1],
        "bio": res[2],
        "telefone": res[3],
        "github": res[4],
        "foto": res[5]  # <--- Aqui está o nome do arquivo
    }
    return render_template("real/pagina_meu_perfil.html", usuario=usuario)


@perfil_bp.route("/atualizar_perfil", methods=["POST"])
@login_required
def atualizar_perfil():
    user_id = session.get("user_id")
    nome = request.form.get("nome")
    bio = request.form.get("bio")
    telefone = request.form.get("telefone")
    github = request.form.get("github")

    foto = request.files.get("foto")
    nome_foto = None

    # Se o usuário enviou uma foto
    if foto and foto.filename != '':
        upload_path = os.path.join("static", "uploads")

        # Garante que a pasta existe
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)

        # Gera um nome seguro (ex: user_1_perfil.jpg)
        extensao = foto.filename.rsplit('.', 1)[1].lower()
        nome_foto = f"user_{user_id}_foto.{extensao}"
        foto.save(os.path.join(upload_path, nome_foto))

    try:
        conn = sqlite3.connect(obter_caminho_banco())
        cursor = conn.cursor()

        if nome_foto:
            cursor.execute("""
                           UPDATE usuarios
                           SET nome     = ?,
                               bio      = ?,
                               telefone = ?,
                               github   = ?,
                               foto     = ?
                           WHERE id = ?
                           """, (nome, bio, telefone, github, nome_foto, user_id))
        else:
            cursor.execute("""
                           UPDATE usuarios
                           SET nome     = ?,
                               bio      = ?,
                               telefone = ?,
                               github   = ?
                           WHERE id = ?
                           """, (nome, bio, telefone, github, user_id))

        conn.commit()
        conn.close()

        # Atualiza o nome na sessão para a Navbar mudar na hora
        session["user_name"] = nome
        flash("Perfil atualizado com sucesso!", "success")

    except Exception as e:
        flash(f"Erro ao salvar no banco: {str(e)}", "error")

    return redirect(url_for("perfil.pagina_meu_perfil"))
