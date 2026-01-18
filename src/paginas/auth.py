from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.banco import registrar_usuario, autenticar_usuario

auth_bp = Blueprint("auth", __name__)

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

    return render_template("pagina_registro.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        usuario = autenticar_usuario(email, senha)
        if usuario:
            session["usuario_id"] = usuario[0]
            session["usuario_nome"] = usuario[1]
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("index.pagina_index"))
        else:
            flash("Email ou senha inválidos.", "error")
            return redirect(url_for("auth.login"))

    # 🔹 Não precisa passar 'usuario' aqui
    return render_template("pagina_login.html")



@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logout realizado com sucesso!")
    return redirect(url_for("index.pagina_index"))
