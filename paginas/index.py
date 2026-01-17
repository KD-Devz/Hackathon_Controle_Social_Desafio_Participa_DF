from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages
from utils import normalizar_ao_retirar_acentuacao_e_cedilha, limpar_texto, termos_sensiveis, variacoes_verbos

index_bp = Blueprint("index", __name__)

@index_bp.route("/", methods=["GET", "POST"])
def pagina_index():
    if request.method == "POST":
        menssagem = request.form.get("menssagem")
        if menssagem:
            linhas = [linha.strip() for linha in menssagem.split('.') if linha.strip()]
            resultado_linhas = []
            status_global = "False"

            for linha in linhas:
                linha_normalizada = normalizar_ao_retirar_acentuacao_e_cedilha(linha)
                linha_normalizada = limpar_texto(linha_normalizada)

                palavras = linha_normalizada.split()
                encontrados = [termo for termo in termos_sensiveis if termo in palavras]

                verbos_encontrados = []
                for forma, infinitivo in variacoes_verbos:
                    if forma in linha_normalizada:
                        verbos_encontrados.append(infinitivo)

                if encontrados and verbos_encontrados:
                    status = "True"
                    status_global = "True"
                else:
                    status = "False"

                resultado_linhas.append({
                    "texto": linha,
                    "status": status,
                    "encontrados": encontrados,
                    "verbos": list(set(verbos_encontrados))
                })

            resposta = {"STATUS": status_global, "linhas": resultado_linhas}
            flash(resposta)
            return redirect(url_for("index.pagina_index"))

    mensagens = get_flashed_messages()
    resposta = mensagens[0] if mensagens else None
    return render_template("pagina_index.html", resposta=resposta)
