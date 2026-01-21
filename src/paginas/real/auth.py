from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.utils.banco import registrar_usuario, autenticar_usuario

auth_bp = Blueprint("auth", __name__)

# No topo do auth.py, ajuste o decorador
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:  # Use 'user_id' aqui
            flash("Você precisa estar logado para acessar o perfil.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")

        if registrar_usuario(nome, email, senha):
            flash("Usuário registrado com sucesso!", "success")
            return redirect(url_for("auth.login"))
        else:
            flash("Email já cadastrado, tente com outro email!", "error")
            return redirect(url_for("auth.registro"))

    return render_template("real/pagina_registro.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        usuario = autenticar_usuario(email, senha)

        if usuario:
            session["user_id"] = usuario[0]
            session["user_name"] = usuario[1]
            # Salve explicitamente se estiver em ambiente de teste
            session.permanent = False

            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("perfil.pagina_meu_perfil"))
        else:
            flash("Email ou senha inválidos.", "error")
    return render_template("real/pagina_login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Sessão encerrada com sucesso!", "success")
    return redirect(url_for("index.pagina_index"))