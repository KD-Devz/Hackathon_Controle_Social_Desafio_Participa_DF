import os
import csv

from src.utils.conjugador import gerar_lista_variacoes
from src.utils.banco import registrar_palavra_proibida

from src.utils.texto import (
    normalizar_ao_retirar_acentuacao_e_cedilha,
    limpar_texto,
)


def carregar_termos_sensiveis():
    raiz = os.path.dirname(os.path.dirname(__file__))
    caminho = os.path.join(raiz, "../validadores", "dados_sensiveis.txt")

    with open(caminho, "r", encoding="utf-8") as f:
        termos = [linha.strip().upper() for linha in f if linha.strip()]
    return termos


def carregar_interrogativas():
    with open("validadores/palavras_interrogativas.txt", "r", encoding="utf-8") as f:
        return [linha.strip().upper() for linha in f if linha.strip()]


# Variáveis globais que podem ser importadas em outros módulos

termos_sensiveis = carregar_termos_sensiveis()
variacoes_verbos = gerar_lista_variacoes()  # lista de pares (forma_conjugada, infinitivo)
palavras_interrogativas = carregar_interrogativas()


def processar_index(mensagem: str):
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


import re


def validar_padroes_sensiveis(texto):
    resultados = {
        "CPFS": [],
        "CNPJS": [],
        "RGS": [],
        "CEPS": []
    }

    # CPF: 000.000.000-00 ou 00000000000
    padrao_cpf = r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b'

    # CNPJ: 00.000.000/0000-00 ou 00000000000000
    padrao_cnpj = r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b'

    # RG (Padrão variado, mas focado em sequências numéricas comuns de 7 a 9 dígitos)
    padrao_rg = r'\b\d{1,2}\.?\d{3}\.?\d{3}-?[\dX]\b'

    # CEP: 00000-000 ou 00000000
    padrao_cep = r'\b\d{5}-?\d{3}\b'

    resultados["CPFS"] = re.findall(padrao_cpf, texto)
    resultados["CNPJS"] = re.findall(padrao_cnpj, texto)
    resultados["RGS"] = re.findall(padrao_rg, texto)
    resultados["CEPS"] = re.findall(padrao_cep, texto)

    return resultados