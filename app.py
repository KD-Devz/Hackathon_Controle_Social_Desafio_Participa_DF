from flask import Flask
from paginas import index_bp, testes_bp

app = Flask(__name__)
app.secret_key = "Hackathon Controle Social - Desafio Participa DF"

# registra os blueprints
app.register_blueprint(index_bp)
app.register_blueprint(testes_bp)

if __name__ == "__main__":
    app.run(debug=True)
