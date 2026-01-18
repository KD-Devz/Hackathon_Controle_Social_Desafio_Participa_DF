# Hackathon Controle Social - Desafio Participa DF

Este projeto foi desenvolvido durante o **Hackathon Controle Social - Desafio Participa DF** e tem como objetivo criar um sistema de validação e análise de solicitações feitas via e-SIC (Sistema Eletrônico do Serviço de Informação ao Cidadão).  

O sistema identifica **dados sensíveis**, **verbos de solicitação** e **palavras interrogativas** em mensagens, classificando se uma solicitação pode ou não ser atendida de acordo com critérios da Lei de Acesso à Informação.

---

## 🚀 Funcionalidades

- **Validação de mensagens (Página Principal)**  
  - Normalização e limpeza de texto.  
  - Identificação de termos sensíveis.  
  - Detecção de verbos de solicitação (com conjugação verbal).  
  - Reconhecimento de palavras interrogativas.  
  - Classificação automática da solicitação como **Válida** ou **Inválida**.  

- **Testes em massa (Página de Testes)**  
  - Carregamento de um arquivo CSV com solicitações.  
  - Processamento em lote com estatísticas de válidos e inválidos.  
  - Exibição dos resultados em tabela e gráfico (Chart.js).  

- **Ranking (Página de Ranking)**  
  - Consulta ao banco SQLite.  
  - Exibição das palavras sensíveis mais buscadas.  
  - Gráfico com os 10 termos mais recorrentes.  

- **Refatoração do código**  
  - Criação de `carregador.py` para centralizar a lógica de análise.  
  - Separação das páginas em Blueprints (`index`, `testes`, `ranking`).  
  - Código mais limpo e reutilizável.  

---

## 🛠️ Tecnologias utilizadas

- **Python 3.10+**  
- **Flask** (Blueprints, rotas e templates)  
- **SQLite3** (armazenamento de termos sensíveis e ranking)  
- **HTML + CSS (PureCSS)**  
- **Chart.js** (gráficos)  
- **CSV** para amostras de testes  

---

## 📊 Exemplo de uso

### Página Principal
- O usuário digita uma solicitação.  
- O sistema valida e retorna se é **atendível** ou **não atendível**, destacando termos sensíveis, verbos e interrogativas.  

### Página de Testes
- Carrega um arquivo CSV com várias solicitações.  
- Exibe estatísticas de válidos e inválidos.  
- Mostra um gráfico com a distribuição.  

### Página de Ranking
- Consolida os resultados e mostra os termos mais recorrentes.  

---

## ▶️ Como executar

1. **Clonar o repositório**
```bash
git clone https://github.com/KD-Devz/Hackathon_Controle_Social_Desafio_Participa_DF.git
cd Hackathon_Controle_Social_Desafio_Participa_DF
```
Instalar Dependências
```bash
pip install -r requirements.txt
```

Executar o projeto

```bash
python3 app.py
```

Acesse no navegador:

Link: http://127.0.0.1:5000/

## 👨‍💻 Autores

Projeto desenvolvido por [CalebeAF02](https://github.com/CalebeAF02) e [DyogoQ](https://github.com/DyogoQ) durante o [Hackathon Controle Social - Desafio Participa DF](https://www.cg.df.gov.br/w/1-hackathon-em-controle-social-desafio-participa-df).

---