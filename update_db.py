import sqlite3
import os

# 1. Caminho para o seu banco atual
# (Ajuste para o caminho onde está o seu arquivo .db)
DB_PATH = "dados/banco.db"

def atualizar_meu_banco():
    if not os.path.exists(DB_PATH):
        print("Erro: Arquivo de banco não encontrado no caminho especificado!")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Lista de "puxadinhos" que precisamos fazer na tabela
    novas_colunas = [
        "ALTER TABLE usuarios ADD COLUMN bio TEXT",
        "ALTER TABLE usuarios ADD COLUMN telefone TEXT",
        "ALTER TABLE usuarios ADD COLUMN github TEXT",
        "ALTER TABLE usuarios ADD COLUMN foto TEXT"
    ]

    for comando in novas_colunas:
        try:
            cursor.execute(comando)
            print(f"Sucesso: {comando}")
        except sqlite3.OperationalError:
            # Se você rodar o script duas vezes, ele cai aqui
            # avisando que a coluna já existe.
            print(f"Aviso: Coluna já existente ou erro no comando.")

    conn.commit()
    conn.close()
    print("--- Banco de dados atualizado com sucesso! ---")

if __name__ == "__main__":
    atualizar_meu_banco()