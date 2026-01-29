# src/paginas/real/documentacao.py
import sqlite3
from io import BytesIO
from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file,
    current_app,
)

# Importa funções do módulo de banco (ajuste o caminho se necessário)
from src.utils.banco import (
    obter_caminho_banco,
    listar_comentarios_documentacao,
    inserir_comentario_documentacao,
)

doc_bp = Blueprint("documentacao", __name__, template_folder="../../../templates/real")


@doc_bp.route("/documentacao", methods=["GET"])
def pagina_documentacao():
    """
    Renderiza a página de documentação e lista os comentários públicos.
    """
    try:
        comentarios = listar_comentarios_documentacao(limit=200)
    except Exception:
        # Em caso de erro ao acessar o banco, loga e mostra lista vazia
        current_app.logger.exception("Erro ao listar comentários da documentação")
        comentarios = []

    return render_template("pagina_documentacao.html", comentarios=comentarios)


@doc_bp.route("/documentacao/comentar", methods=["POST"])
def comentar_documentacao():
    """
    Recebe um comentário via POST e salva no banco.
    """
    nome = request.form.get("nome", "").strip() or None
    comentario = request.form.get("comentario", "").strip()

    if not comentario:
        flash("Comentário vazio.", "error")
        return redirect(url_for("documentacao.pagina_documentacao"))

    criado_em = datetime.utcnow().isoformat()

    try:
        inserir_comentario_documentacao(nome, comentario, criado_em)
    except Exception:
        current_app.logger.exception("Erro ao inserir comentário")
        flash("Erro ao salvar comentário. Tente novamente mais tarde.", "error")
        return redirect(url_for("documentacao.pagina_documentacao"))

    flash("Comentário enviado. Obrigado pelo feedback!", "success")
    return redirect(url_for("documentacao.pagina_documentacao")+ "#contribuir")


@doc_bp.route("/documentacao/pdf", methods=["GET"])
def documentacao_pdf():
    now = datetime.utcnow()
    resumo_html = render_template("pagina_documentacao_pdf.html", now=now)

    try:
        from xhtml2pdf import pisa  # pip install xhtml2pdf

        pdf = BytesIO()
        pisa_status = pisa.CreatePDF(resumo_html, dest=pdf)
        if pisa_status.err:
            current_app.logger.error("xhtml2pdf retornou erro ao gerar PDF")
            flash("Erro ao gerar PDF.", "error")
            return redirect(url_for("documentacao.pagina_documentacao"))

        pdf.seek(0)
        filename = "documentacao_resumida.pdf"
        # send_file com download_name (Flask >= 2.0). Se usar versão antiga, substitua por attachment_filename.
        return send_file(pdf, mimetype="application/pdf", as_attachment=True, download_name=filename)
    except Exception:
        current_app.logger.exception("Erro ao gerar PDF (xhtml2pdf).")
        flash("Geração de PDF não disponível (verifique dependências).", "error")
        return redirect(url_for("documentacao.pagina_documentacao"))
