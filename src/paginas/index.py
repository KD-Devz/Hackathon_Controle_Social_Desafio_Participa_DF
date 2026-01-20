from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages, session
from src.utils.carregador import processar_index
import sqlite3

index_bp = Blueprint("index", __name__)

@index_bp.route("/", methods=["GET", "POST"])
def pagina_index():
    return render_template("pagina_index.html")

@index_bp.route("/enviar_comentario", methods=["POST"])
def enviar_comentario():
    comentario = request.form.get("comentario", "").strip()
    if not comentario:
        flash("O comentário não pode estar vazio.", "error")
        return redirect(url_for("index.pagina_index"))

    flash("Comentário enviado com sucesso!", "success")
    return redirect(url_for("index.pagina_index"))