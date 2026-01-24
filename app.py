from flask import Flask
from src.utils.banco import inicializar_banco
from src.paginas import index_bp, testes_bp, ranking_bp, testes_detalhados_bp, perfil_bp, auth_bp, solicitacao_bp, doc_bp
from datetime import timedelta

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = "Hackathon Controle Social"

inicializar_banco()
app.register_blueprint(index_bp)
app.register_blueprint(testes_bp)
app.register_blueprint(ranking_bp)
app.register_blueprint(testes_detalhados_bp)
app.register_blueprint(perfil_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(solicitacao_bp)
app.register_blueprint(doc_bp)

if __name__ == "__main__":
    app.run(debug=True)

# No seu app.py
app.config.update(
    SESSION_PERMANENT = False,
    SESSION_TYPE = 'filesystem' # Opcional: força o Flask a gerenciar melhor o estado
)

app.permanent_session_lifetime = timedelta(minutes=60) # Expira em 10 min de inatividade