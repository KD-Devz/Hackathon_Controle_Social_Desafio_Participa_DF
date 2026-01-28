import os
import csv
from src.utils.conjugador import gerar_lista_variacoes
from src.utils.texto import normalizar_ao_retirar_acentuacao_e_cedilha

def carregar_csv(arquivo):
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho = os.path.join(raiz, "../validadores", arquivo)

    linhas = []

    with open(caminho, newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            cont = 0
            for linha in row:
                if cont == 0:
                    linhas.append(linha)
                cont += 1
    return linhas

def carregar_txt(arquivo):
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho = os.path.join(raiz, "../validadores", arquivo)

    with open(caminho, "r", encoding="utf-8") as f:
        termos = [normalizar_ao_retirar_acentuacao_e_cedilha(linha.strip().upper()) for linha in f if linha.strip()]
    return termos

def carregar_termos_sensiveis():
    return carregar_txt("dados_sensiveis.txt")

def carregar_interrogativas():
    return carregar_txt("palavras_interrogativas.txt")

def carregar_sobrenomes():
    lista = []

    for local_sobrenomes in carregar_txt("sobrenomes.txt"):
        for sobrenome in local_sobrenomes.split(" "):
            termo = normalizar_ao_retirar_acentuacao_e_cedilha(sobrenome)
            if len(termo) > 2:
                lista.append(termo)

    return lista

def carregar_nomes():
    lista = []
    for nome in carregar_csv("ibge_nomes_femininos.csv"):
        termo = normalizar_ao_retirar_acentuacao_e_cedilha(nome.upper())
        if len(termo)>2:
            lista.append(termo)
    for nome in carregar_csv("ibge_nomes_masculinos.csv"):
        termo = normalizar_ao_retirar_acentuacao_e_cedilha(nome.upper())
        if len(termo)>2:
            lista.append(termo)

    return lista

class RecursosLinguisticos:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            # inicializa apenas uma vez
            cls._instancia.termos_sensiveis = carregar_termos_sensiveis()
            cls._instancia.variacoes_verbos = gerar_lista_variacoes()
            cls._instancia.palavras_interrogativas = carregar_interrogativas()
            cls._instancia.sobrenomes = carregar_sobrenomes()
            cls._instancia.nomes = carregar_nomes()
        return cls._instancia

