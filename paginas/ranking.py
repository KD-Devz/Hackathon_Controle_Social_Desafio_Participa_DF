import sqlite3
from flask import Blueprint, render_template
from utils import termos_sensiveis

ranking_bp = Blueprint("ranking", __name__)

@ranking_bp.route("/ranking")
def pagina_ranking():
    # Conecta ao banco SQLite
    conn = sqlite3.connect("banco.db")  # ajuste o caminho se necessário
    cursor = conn.cursor()

    # Busca todas as palavras e suas quantidades
    cursor.execute("SELECT palavra, quantidade FROM palavras_proibidas_mais_buscadas")
    resultados = cursor.fetchall()
    conn.close()

    # Filtra apenas palavras que estão nos termos sensíveis
    resultados_filtrados = [(palavra, qtd) for palavra, qtd in resultados if palavra.upper() in termos_sensiveis]

    # Ordena por quantidade decrescente e pega as 3 primeiras
    top3 = sorted(resultados_filtrados, key=lambda x: x[1], reverse=True)[:10]

    # Separa listas para o gráfico
    palavras = [p for p, _ in top3]
    quantidades = [q for _, q in top3]

    return render_template("pagina_ranking.html", palavras=palavras, quantidades=quantidades)
