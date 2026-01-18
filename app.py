from flask import Flask

from src.banco import inicializar_banco
from src.paginas import index_bp, testes_bp, ranking_bp, testes_detalhados_bp, perfil_bp, auth_bp, enviar_solicitacao_bp

app = Flask(__name__)
app.secret_key = "Hackathon Controle Social - Desafio Participa DF"

inicializar_banco()
app.register_blueprint(index_bp)
app.register_blueprint(testes_bp)
app.register_blueprint(ranking_bp)
app.register_blueprint(testes_detalhados_bp)

app.register_blueprint(perfil_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(enviar_solicitacao_bp)


if __name__ == "__main__":
    app.run(debug=True)
