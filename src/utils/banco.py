import hashlib
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

    cursor.execute(""" CREATE TABLE IF NOT EXISTS usuarios
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           nome
                           TEXT
                           NOT
                           NULL,
                           email
                           TEXT
                           UNIQUE
                           NOT
                           NULL,
                           senha
                           TEXT
                           NOT
                           NULL
                       ) """)

    cursor.execute(""" CREATE TABLE IF NOT EXISTS solicitacoes
    (
        id
        INTEGER
        PRIMARY
        KEY
        AUTOINCREMENT,
        usuario_id
        INTEGER
        NOT
        NULL,
        texto
        TEXT
        NOT
        NULL,
        data_envio
        TIMESTAMP
        DEFAULT
        CURRENT_TIMESTAMP,
        FOREIGN
        KEY
                       (
        usuario_id
                       ) REFERENCES usuarios
                       (
                           id
                       ) ) """)

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
    caminho = os.path.join(raiz, "../dados", "banco.db")
    return caminho


def registrar_usuario(nome: str, email: str, senha: str):
    conn = sqlite3.connect(obter_caminho_banco())
    cursor = conn.cursor()

    # Criptografa a senha com SHA256
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    try:
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha_hash))
        conn.commit()
        sucesso = True
    except sqlite3.IntegrityError:
        # Email já existe
        sucesso = False

    conn.close()
    return sucesso


def autenticar_usuario(email: str, senha: str):
    conn = sqlite3.connect(obter_caminho_banco())
    cursor = conn.cursor()

    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha_hash))
    usuario = cursor.fetchone()

    conn.close()
    return usuario  # retorna None se não encontrar
