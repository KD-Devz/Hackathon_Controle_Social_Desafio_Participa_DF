import sqlite3
from flask import Blueprint, render_template, session, redirect, url_for, flash
from src.utils.banco import obter_caminho_banco
from src.paginas.real.auth import login_required
perfil_bp = Blueprint("perfil", __name__)


@perfil_bp.route("/meu_perfil")
@login_required
def pagina_meu_perfil():
    # 🔹 Verifica se o usuário está logado
    if "usuario_id" not in session:
        flash("Você precisa estar logado para acessar o perfil.")
        return redirect(url_for("auth.login"))

    usuario_id = session["usuario_id"]

    # 🔹 Busca informações do usuário no banco
    conn = sqlite3.connect(obter_caminho_banco())
    cursor = conn.cursor()
    cursor.execute("SELECT nome, email FROM usuarios WHERE id = ?", (usuario_id,))
    resultado = cursor.fetchone()
    conn.close()

    if not resultado:
        flash("Usuário não encontrado.")
        return redirect(url_for("auth.login"))

    usuario = {
        "nome": resultado[0],
        "email": resultado[1]
    }

    return render_template("real/pagina_meu_perfil.html", usuario=usuario)
