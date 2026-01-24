# Valida Fácil

Este projeto foi desenvolvido durante o **Hackathon Controle Social** e tem como objetivo criar
um sistema de validação e análise de solicitações feitas via e-SIC (Sistema Eletrônico do Serviço de Informação ao
Cidadão).

O sistema identifica **dados sensíveis**, **verbos de solicitação** e **palavras interrogativas** em mensagens,
classificando se uma solicitação pode ou não ser atendida de acordo com critérios da Lei de Acesso à Informação (LAI) e
em conformidade com a LGPD.

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

- **Teste Detalhado**
  - Exibição da análise de uma linha específica do CSV.
  - Mostra status, termos sensíveis, verbos e interrogativas.

- **Perfil**
  - Página dedicada ao usuário, exibindo informações básicas (nome, email, cargo, instituição, descrição).

- **Documentação Técnica**
  - Painel interativo com tópicos de arquitetura, instalação, execução, formatos, metodologia, segurança e API.
  - Área de comunidade para feedback técnico.

- **Refatoração do código**
  - Criação de `carregador.py` para centralizar a lógica de análise.
  - Separação das páginas em Blueprints (`index`, `testes`, `ranking`, `testes_detalhados`, `perfil`, `documentacao`).
  - Código mais limpo e reutilizável.

---

## 🛠️ Tecnologias utilizadas

- **Python 3.11+**
- **Flask** (Blueprints, rotas e templates)
- **SQLite3** (armazenamento de termos sensíveis e ranking)
- **HTML + CSS (PureCSS + custom styles)**
- **Chart.js** (gráficos dinâmicos)
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

### Página de Teste Detalhado
- Permite visualizar a análise de uma linha específica do CSV.
- Exibe status, termos sensíveis, verbos e interrogativas.

### Página de Perfil
- Exibe informações básicas do usuário em layout centralizado.

### Página de Documentação
- Exibe tópicos técnicos organizados em painel lateral.
- Permite navegação entre arquitetura, instalação, execução, formatos, metodologia, segurança e API.
- Área de comunidade para comentários e sugestões.

---

## ▶️ Como executar

1. **Clonar o repositório**
 ```bash
 git clone https://github.com/CalebeAF02/Hackathon_Controle_Social_Desafio_Participa_DF.git
 cd Hackathon_Controle_Social_Desafio_Participa_DF


2. **Configura o Ambiente**
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. **Instalar Dependências**
```bash
pip install -r requirements.txt
```

4. **Executar o projeto**
```bash
python3 app.py
```

**Acesse no navegador:**

Link: http://127.0.0.1:5000/

## 👨‍💻 Autores

Projeto desenvolvido por [CalebeAF02](https://github.com/CalebeAF02) e [DyogoQ](https://github.com/DyogoQ) durante
o [Hackathon Controle Social - Desafio Participa DF](https://www.cg.df.gov.br/w/1-hackathon-em-controle-social-desafio-participa-df).

---