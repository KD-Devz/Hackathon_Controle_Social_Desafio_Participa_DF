import os
import unicodedata

def remover_acentos(texto: str) -> str:
    """Remove acentos e substitui 'ç' por 'c'."""
    texto = unicodedata.normalize("NFD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")
    return texto.replace("Ç", "C").replace("ç", "c")


def carregar_verbos(caminho_arquivo):
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        linhas = [remover_acentos(linha.strip().upper()) for linha in f if linha.strip()]
    return linhas


def gerar_variacoes_verbo_regular(verbo: str):
    """Gera algumas variações comuns de conjugação para verbos regulares terminados em -AR."""
    radical = verbo[:-2]  # remove 'AR'
    formas = [
        verbo,
        radical + "O", radical + "A", radical + "AMOS", radical + "AM",
        radical + "AVA", radical + "AVAM", radical + "AVAMOS",
        radical + "EI", radical + "OU", radical + "ARAM",
        radical + "AREI", radical + "ARA", radical + "AREMOS", radical + "ARAO",
        radical + "E", radical + "EM", radical + "ES",
    ]
    # Remove acentos de cada forma
    return [(remover_acentos(forma), verbo) for forma in formas]


def carregar_verbos_irregulares():
    """
    Cada linha do arquivo verbos_de_solicitacao_irregular.txt deve ter:
    INFINITIVO forma1 forma2 forma3 ...
    """
    caminho = os.path.join(os.path.dirname(__file__), "../../validadores", "verbos_de_solicitacao_irregular.txt")
    variacoes = []
    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            partes = remover_acentos(linha.strip().upper()).split()
            if not partes:
                continue
            infinitivo = partes[0]
            formas = partes[1:]
            for forma in formas:
                variacoes.append((remover_acentos(forma), infinitivo))
            variacoes.append((infinitivo, infinitivo))
    return variacoes


def gerar_lista_variacoes():
    base_dir = os.path.dirname(__file__)
    regulares = carregar_verbos(os.path.join(base_dir, "../../validadores", "verbos_de_solicitacao_regular.txt"))
    irregulares = carregar_verbos_irregulares()

    variacoes = []
    for verbo in regulares:
        variacoes.extend(gerar_variacoes_verbo_regular(verbo))
    variacoes.extend(irregulares)

    return variacoes
