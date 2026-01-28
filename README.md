# 🛡️ Privacy Shield — Valida Fácil

O **Privacy Shield** é uma solução de inteligência de dados desenvolvida durante o **Hackathon Controle Social (Desafio Participa DF)**. O sistema atua como um sentinela entre as solicitações de informação (e-SIC) e a administração pública, filtrando automaticamente dados sensíveis em conformidade com a **LGPD** e a **LAI**.

---

## 🎯 Objetivo do Projeto
Nossa missão é automatizar a triagem de pedidos de informação pública no GDF. O sistema identifica riscos de exposição de dados pessoais (PII) e analisa a real intenção da solicitação através de processamento linguístico, garantindo segurança jurídica aos gestores e rapidez ao cidadão.

---

## 🚀 O Diferencial Tecnológico
Diferente de filtros de texto comuns, nossa solução utiliza uma abordagem multicamadas:

* **Validação Algorítmica (Módulo 11):** O sistema aplica cálculos matemáticos para validar se um CPF ou CNPJ é real, evitando bloqueios por números aleatórios.
* **Análise Semântica de Verbos:** Através de um motor de conjugação própria (`conjugador.py`), identificamos a intenção de solicitações (ex: "querer", "exigir", "solicitar") em qualquer tempo verbal.
* **Reconhecimento de Identidade (IBGE):** Cruzamento dinâmico com bases de nomes e sobrenomes para detectar e anonimizar nomes próprios em textos não estruturados.
* **Monitoramento de Riscos:** Consolidação em banco SQLite3 dos termos sensíveis detectados, gerando indicadores de vulnerabilidade para o órgão.

---

## ✨ Funcionalidades

### 🛡️ Auditoria em Tempo Real (Página Principal)
* **Motor Híbrido:** Normalização e limpeza de texto (remoção de ruídos e acentuação).
* **Detecção de Padrões:** Identificação de termos sensíveis, documentos e palavras interrogativas.
* **Veredito Automático:** Classificação instantânea da solicitação como **Válida** ou **Inválida**.

### 🧪 Testes de Stress e Massa (Página de Testes)
* **Processamento em Lote:** Upload de arquivos CSV para auditoria de grandes volumes de dados simultaneamente.
* **Analytics Visual:** Dashboards dinâmicos com estatísticas de conformidade gerados via **Chart.js**.

### 📈 Inteligência de Riscos (Ranking)
* **Auditoria de Termos:** Monitoramento das palavras sensíveis mais buscadas.
* **Inspeção Cirúrgica:** Visualização detalhada de linhas específicas para análise minuciosa de verbos e interrogativas.

### 📑 Governança e Perfil
* **Portal Técnico:** Painel interativo com tópicos de arquitetura, metodologia e API Reference.
* **Perfil do Auditor:** Gestão de informações (nome, cargo, bio) e controle de acesso.
* **Clean Code:** Estrutura modular baseada em **Blueprints** e lógica centralizada no `carregador.py`.

---

## 🛠️ Tecnologias Utilizadas

| Camada | Tecnologia |
| :--- | :--- |
| **Backend** | Python 3.11+ |
| **Framework** | Flask (Blueprints & Jinja2) |
| **Banco de Dados** | SQLite 3 |
| **Frontend** | Interface Responsiva (Glow Design) & Chart.js |
| **Segurança** | Criptografia SHA-256 para credenciais |

---

## 📊 Exemplo de Operação

1. **Entrada:** O usuário insere uma solicitação no e-SIC.
2. **Processamento:** O sistema valida documentos via **Módulo 11**, cruza nomes com a base do **IBGE** e conjuga os verbos de ação.
3. **Saída:** O sistema destaca os termos críticos e define se o pedido é **Atendível** ou **Não Atendível**, protegendo a privacidade do cidadão.

---

## ▶️ Como executar

1. **Clonar o repositório**
 ```bash
 git clone https://github.com/CalebeAF02/Hackathon_Controle_Social_Desafio_Participa_DF.git
 
 cd Hackathon_Controle_Social_Desafio_Participa_DF
```

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

"Garantir a transparência sem sacrificar a privacidade."
---