from flask import Flask
from paginas import index_bp, testes_bp, ranking_bp
from utils import inicializar_banco
app = Flask(__name__)
app.secret_key = "Hackathon Controle Social - Desafio Participa DF"

# inicializa o banco
inicializar_banco()

# registra os blueprints
app.register_blueprint(index_bp)
app.register_blueprint(testes_bp)
app.register_blueprint(ranking_bp)

if __name__ == "__main__":
    app.run(debug=True)
