from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages

app = Flask(__name__)
app.secret_key = "segredo-super-seguro"  # necessário para usar flash

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        menssagem = request.form.get("menssagem")
        if menssagem:
            status = "True" if "CPF" in menssagem.upper() else "False"
            resposta = {"STATUS": status, "menssagem": menssagem}
            # guarda a resposta como flash message
            flash(resposta)
            return redirect(url_for("index"))

    # recupera mensagens flash (se houver)
    mensagens = get_flashed_messages()
    resposta = mensagens[0] if mensagens else None

    return render_template("index.html", resposta=resposta)

if __name__ == "__main__":
    app.run(debug=True)
