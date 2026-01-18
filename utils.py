import os
import unicodedata
import re
from conjugador import gerar_lista_variacoes
import sqlite3

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

def carregar_interrogativas():
    with open("validadores/palavras_interrogativas.txt", "r", encoding="utf-8") as f:
        return [linha.strip().upper() for linha in f if linha.strip()]

palavras_interrogativas = carregar_interrogativas()

def inicializar_banco():
    """
    Cria o banco de dados SQLite e a tabela 'palavras_proibidas_mais_buscadas'
    caso ainda não existam.
    """
    caminho_banco = "banco.db"  # ajuste o caminho se necessário

    # Conecta (se não existir, o arquivo será criado)
    conn = sqlite3.connect(caminho_banco)
    cursor = conn.cursor()

    # Cria a tabela se não existir
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS palavras_proibidas_mais_buscadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            palavra TEXT NOT NULL,
            quantidade INTEGER NOT NULL DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

import sqlite3

def registrar_palavra_proibida(palavra: str):
    """
    Insere ou atualiza a quantidade de uma palavra proibida na tabela.
    """
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    # Se já existe, incrementa; senão insere
    cursor.execute("""
        SELECT quantidade FROM palavras_proibidas_mais_buscadas WHERE palavra = ?
    """, (palavra,))
    resultado = cursor.fetchone()

    if resultado:
        nova_qtd = resultado[0] + 1
        cursor.execute("""
            UPDATE palavras_proibidas_mais_buscadas SET quantidade = ? WHERE palavra = ?
        """, (nova_qtd, palavra))
    else:
        cursor.execute("""
            INSERT INTO palavras_proibidas_mais_buscadas (palavra, quantidade) VALUES (?, ?)
        """, (palavra, 1))

    conn.commit()
    conn.close()
