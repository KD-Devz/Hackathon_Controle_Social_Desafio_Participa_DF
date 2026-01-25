import hashlib
import os
import sqlite3
from typing import Optional, Tuple

# Caminho absoluto para o arquivo do banco (projeto_root/dados/banco.db)
def obter_caminho_banco() -> str:
    # __file__ -> src/utils/banco.py
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    dados_dir = os.path.join(base_dir, "dados")
    os.makedirs(dados_dir, exist_ok=True)
    return os.path.join(dados_dir, "banco.db")


def _hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


def inicializar_banco() -> None:
    db_path = obter_caminho_banco()
    # Garante que a pasta exista (obter_caminho_banco já faz isso, mas reforça)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS palavras_proibidas_mais_buscadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            palavra TEXT NOT NULL,
            quantidade INTEGER NOT NULL DEFAULT 0
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS solicitacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            texto TEXT NOT NULL,
            data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS comentarios_documentacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            comentario TEXT NOT NULL,
            criado_em TEXT NOT NULL
        )
        """)

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS solicitacoes_anonimas
                       (
                           id         INTEGER PRIMARY KEY AUTOINCREMENT,
                           texto      TEXT     NOT NULL,
                           data_envio DATETIME NOT NULL
                       )
                       """)

        conn.commit()


def registrar_palavra_proibida(palavra: str) -> None:
    db_path = obter_caminho_banco()
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT quantidade FROM palavras_proibidas_mais_buscadas WHERE palavra = ?
        """, (palavra,))
        row = cursor.fetchone()
        if row:
            nova_qtd = row[0] + 1
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


def registrar_usuario(nome: str, email: str, senha: str) -> bool:
    """
    Registra um usuário. Retorna True se sucesso, False se email já existir.
    A senha é armazenada como hash SHA256.
    """
    db_path = obter_caminho_banco()
    senha_hash = _hash_senha(senha)
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
                (nome, email, senha_hash)
            )
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        # email já cadastrado (constraint UNIQUE)
        return False


def autenticar_usuario(email: str, senha: str) -> Optional[Tuple]:
    """
    Autentica usuário por email e senha.
    Retorna a tupla do usuário (id, nome, email, senha_hash) se encontrado, ou None.
    """
    db_path = obter_caminho_banco()
    senha_hash = _hash_senha(senha)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, email, senha FROM usuarios WHERE email = ? AND senha = ?", (email, senha_hash))
        usuario = cursor.fetchone()
    return usuario


def obter_usuario_por_id(usuario_id: int) -> Optional[Tuple]:
    db_path = obter_caminho_banco()
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, email FROM usuarios WHERE id = ?", (usuario_id,))
        row = cursor.fetchone()
    return row


def listar_comentarios_documentacao(limit: int = 200):
    db_path = obter_caminho_banco()
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nome, comentario, criado_em
            FROM comentarios_documentacao
            ORDER BY criado_em DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
    comentarios = [
        {"id": r[0], "nome": r[1] or "Anônimo", "comentario": r[2], "criado_em": r[3]}
        for r in rows
    ]
    return comentarios


def inserir_comentario_documentacao(nome: Optional[str], comentario: str, criado_em: str) -> None:
    db_path = obter_caminho_banco()
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO comentarios_documentacao (nome, comentario, criado_em)
            VALUES (?, ?, ?)
        """, (nome, comentario, criado_em))
        conn.commit()
