from flask import Blueprint, render_template

perfil_bp = Blueprint("perfil", __name__)


@perfil_bp.route("/meu_perfil")
def pagina_meu_perfil():
    # Exemplo de dados do perfil (poderia vir do banco de dados futuramente)
    usuario = {
        "nome": "Calebe",
        "email": "calebe@example.com",
        "cargo": "Desenvolvedor",
        "instituicao": "Hackathon Controle Social - DF",
        "descricao": "Participante ativo do desafio Participa DF, focado em soluções de controle social."
    }
    return render_template("pagina_meu_perfil.html", usuario=usuario)
