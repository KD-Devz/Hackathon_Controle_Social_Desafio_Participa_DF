from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
import os
import unicodedata
from conjugador import gerar_lista_variacoes

app = Flask(__name__)
app.secret_key = "segredo-super-seguro"

# Função para normalizar texto (remover acentos e 'ç')
def normalizar_texto(texto: str) -> str:
    # decompor caracteres acentuados
    nfkd = unicodedata.normalize("NFKD", texto)
    # remover acentos
    sem_acento = "".join([c for c in nfkd if not unicodedata.combining(c)])
    # trocar cedilha por 'c'
    sem_acento = sem_acento.replace("ç", "c").replace("Ç", "C")
    return sem_acento.upper()

# Carrega termos sensíveis
def carregar_termos_sensiveis():
    caminho = os.path.join(os.path.dirname(__file__), "validadores", "dados_sensiveis.txt")
    with open(caminho, "r", encoding="utf-8") as f:
        termos = [linha.strip().upper() for linha in f if linha.strip()]
    return termos

termos_sensiveis = carregar_termos_sensiveis()
variacoes_verbos = gerar_lista_variacoes()  # lista de pares (forma_conjugada, infinitivo)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        menssagem = request.form.get("menssagem")
        if menssagem:
            # divide em linhas pelo ponto
            linhas = [linha.strip() for linha in menssagem.split('.') if linha.strip()]

            resultado_linhas = []
            status_global = "False"

            for linha in linhas:
                linha_normalizada = normalizar_texto(linha)

                # verifica dados sensíveis
                encontrados = [termo for termo in termos_sensiveis if termo in linha_normalizada]

                # procura verbos conjugados e guarda o infinitivo
                verbos_encontrados = []
                for forma, infinitivo in variacoes_verbos:
                    if forma in linha_normalizada:
                        verbos_encontrados.append(infinitivo)

                # só invalida se tiver verbo + dado sensível
                if encontrados and verbos_encontrados:
                    status = "True"
                    status_global = "True"
                else:
                    status = "False"

                resultado_linhas.append({
                    "texto": linha,  # devolve a linha original
                    "status": status,
                    "encontrados": encontrados,
                    "verbos": list(set(verbos_encontrados))  # remove duplicados
                })

            resposta = {"STATUS": status_global, "linhas": resultado_linhas}
            flash(resposta)
            return redirect(url_for("index"))

    mensagens = get_flashed_messages()
    resposta = mensagens[0] if mensagens else None
    return render_template("index.html", resposta=resposta)

if __name__ == "__main__":
    app.run(debug=True)
