import os
import csv
from utils import (
    normalizar_ao_retirar_acentuacao_e_cedilha,
    limpar_texto,
    termos_sensiveis,
    variacoes_verbos,
    registrar_palavra_proibida,
    palavras_interrogativas
)

def processar_index(mensagem: str):
    """
    Processa uma mensagem única (texto do usuário) para a página principal.
    Divide em linhas e retorna a análise.
    """
    linhas = [linha.strip() for linha in mensagem.split('.') if linha.strip()]
    resultado_linhas = []
    status_global = "False"

    for linha in linhas:
        linha_normalizada = normalizar_ao_retirar_acentuacao_e_cedilha(linha)
        linha_normalizada = limpar_texto(linha_normalizada)
        palavras = linha_normalizada.split()

        encontrados = [termo for termo in termos_sensiveis if termo in palavras]
        for termo in encontrados:
            registrar_palavra_proibida(termo)

        verbos_encontrados = [infinitivo for forma, infinitivo in variacoes_verbos if forma in linha_normalizada]
        interrogativas_encontradas = [p for p in palavras_interrogativas if p in palavras]

        if (encontrados and verbos_encontrados) or (encontrados and interrogativas_encontradas):
            status = "True"
            status_global = "True"
        else:
            status = "False"

        resultado_linhas.append({
            "texto": linha,
            "status": status,
            "encontrados": encontrados,
            "verbos": list(set(verbos_encontrados)),
            "interrogativas": interrogativas_encontradas
        })

    return {"STATUS": status_global, "linhas": resultado_linhas}


def processar_testes(caminho_csv: str):
    """
    Processa um arquivo CSV de amostras para a página de testes.
    Retorna os dados analisados e estatísticas.
    """
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
        for termo in encontrados:
            registrar_palavra_proibida(termo)

        verbos_encontrados = [infinitivo for forma, infinitivo in variacoes_verbos if forma in linha_normalizada]
        interrogativas_encontradas = [p for p in palavras_interrogativas if p in palavras]

        if (encontrados and verbos_encontrados) or (encontrados and interrogativas_encontradas):
            status = "Inválido"
            total_invalidos += 1
        else:
            status = "Válido"
            total_validos += 1

        resultado_dados.append({
            "campos": row,
            "status": status,
            "encontrados": encontrados,
            "verbos": list(set(verbos_encontrados)),
            "interrogativas": interrogativas_encontradas
        })

    total_testes = len(dados)

    return {
        "cabecalho": cabecalho,
        "dados": resultado_dados,
        "total_testes": total_testes,
        "total_validos": total_validos,
        "total_invalidos": total_invalidos
    }
