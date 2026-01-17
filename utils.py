import os
import unicodedata
import re
from conjugador import gerar_lista_variacoes

# Função para normalizar texto (remover acentos e 'ç')
def normalizar_ao_retirar_acentuacao_e_cedilha(texto: str) -> str:
    """
    Remove acentos e cedilha de um texto e retorna em maiúsculas.
    """
    nfkd = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join([c for c in nfkd if not unicodedata.combining(c)])
    sem_acento = sem_acento.replace("ç", "c").replace("Ç", "C")
    return sem_acento.upper()

def limpar_texto(texto: str) -> str:
    """
    Remove qualquer caractere que não seja letra, número ou espaço.
    Retorna o texto em maiúsculas.
    """
    apenas_letras_numeros = re.sub(r'[^A-Za-z0-9 ]+', '', texto)
    return apenas_letras_numeros.upper()

def carregar_termos_sensiveis():
    """
    Carrega os termos sensíveis do arquivo 'validadores/dados_sensiveis.txt'.
    Cada termo é convertido para maiúsculas.
    """
    caminho = os.path.join(os.path.dirname(__file__), "validadores", "dados_sensiveis.txt")
    with open(caminho, "r", encoding="utf-8") as f:
        termos = [linha.strip().upper() for linha in f if linha.strip()]
    return termos

# Variáveis globais que podem ser importadas em outros módulos
termos_sensiveis = carregar_termos_sensiveis()
variacoes_verbos = gerar_lista_variacoes()  # lista de pares (forma_conjugada, infinitivo)
