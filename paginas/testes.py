import os
import csv
from flask import Blueprint, render_template
from utils import normalizar_ao_retirar_acentuacao_e_cedilha, limpar_texto, termos_sensiveis, variacoes_verbos

testes_bp = Blueprint("testes", __name__)

@testes_bp.route("/testes")
def pagina_testes():
    caminho_csv = os.path.join(os.path.dirname(__file__), "..", "testes", "AMOSTRA_e-SIC.csv")
    linhas = []
    with open(caminho_csv, newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            linhas.append(row)

    cabecalho = linhas[0]
    dados = linhas[1:]

    resultado_dados = []
    total_validos = 0
    total_invalidos = 0

    for row in dados:
        linha_texto = " ".join(row)
        linha_normalizada = normalizar_ao_retirar_acentuacao_e_cedilha(linha_texto)
        linha_normalizada = limpar_texto(linha_normalizada)

        palavras = linha_normalizada.split()
        encontrados = [termo for termo in termos_sensiveis if termo in palavras]

        verbos_encontrados = []
        for forma, infinitivo in variacoes_verbos:
            if forma in linha_normalizada:
                verbos_encontrados.append(infinitivo)

        if encontrados and verbos_encontrados:
            status = "Inválido"
            total_invalidos += 1
        else:
            status = "Válido"
            total_validos += 1

        resultado_dados.append({
            "campos": row,
            "status": status,
            "encontrados": encontrados,
            "verbos": list(set(verbos_encontrados))
        })

    total_testes = len(dados)

    return render_template(
        "pagina_testes.html",
        cabecalho=cabecalho,
        dados=resultado_dados,
        total_testes=total_testes,
        total_validos=total_validos,
        total_invalidos=total_invalidos
    )
