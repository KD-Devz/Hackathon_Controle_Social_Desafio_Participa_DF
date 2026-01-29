# src/paginas/real/documentacao.py
from datetime import datetime
from io import BytesIO

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
    return redirect(url_for("documentacao.pagina_documentacao") + "#contribuir")


import os


@doc_bp.route("/documentacao/pdf", methods=["GET"])
def documentacao_pdf():
    now = datetime.utcnow()

    # Busca o caminho absoluto da logo para o xhtml2pdf encontrar
    logo_path = os.path.join(current_app.root_path, 'static', 'img', 'logo.png')

    # Se a logo não existir, passamos None para não quebrar o código
    if not os.path.exists(logo_path):
        logo_path = None

    resumo_html = render_template(
        "pagina_documentacao_pdf.html",
        now=now,
        logo_path=logo_path
    )

    try:
        from xhtml2pdf import pisa
        pdf = BytesIO()
        pisa_status = pisa.CreatePDF(resumo_html, dest=pdf)

        if pisa_status.err:
            return "Erro ao gerar PDF", 500

        pdf.seek(0)
        return send_file(
            pdf,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"Relatorio_Tecnico_{now.strftime('%Y%m%d')}.pdf"
        )
    except Exception as e:
        current_app.logger.error(f"Erro PDF: {e}")
        flash("Instale xhtml2pdf para gerar o manual.", "error")
        return redirect(url_for("documentacao.pagina_documentacao"))
