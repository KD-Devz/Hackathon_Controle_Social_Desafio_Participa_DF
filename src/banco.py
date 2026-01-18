import os
import sqlite3


def inicializar_banco():
    conn = sqlite3.connect(obter_caminho_banco())
    cursor = conn.cursor()

    # Cria a tabela se não existir
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS palavras_proibidas_mais_buscadas
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       palavra
                       TEXT
                       NOT
                       NULL,
                       quantidade
                       INTEGER
                       NOT
                       NULL
                       DEFAULT
                       0
                   )
                   """)

    conn.commit()
    conn.close()


def registrar_palavra_proibida(palavra: str):
    conn = sqlite3.connect(obter_caminho_banco())
    cursor = conn.cursor()

    # Se já existe, incrementa; senão insere
    cursor.execute("""
                   SELECT quantidade
                   FROM palavras_proibidas_mais_buscadas
                   WHERE palavra = ?
                   """, (palavra,))
    resultado = cursor.fetchone()

    if resultado:
        nova_qtd = resultado[0] + 1
        cursor.execute("""
                       UPDATE palavras_proibidas_mais_buscadas
                       SET quantidade = ?
                       WHERE palavra = ?
                       """, (nova_qtd, palavra))
    else:
        cursor.execute("""
                       INSERT INTO palavras_proibidas_mais_buscadas (palavra, quantidade)
                       VALUES (?, ?)
                       """, (palavra, 1))

    conn.commit()
    conn.close()


def obter_caminho_banco():
    raiz = os.path.dirname(os.path.dirname(__file__))
    caminho = os.path.join(raiz, "dados", "banco.db")
    return caminho
