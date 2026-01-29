# 🛡️ Privacy Shield — Valida Fácil (v2.0)

O **Privacy Shield** é uma solução de inteligência de dados desenvolvida durante o **Hackathon Controle Social (Desafio Participa DF)**. O sistema atua como um sentinela entre as solicitações de informação (e-SIC) e a administração pública, filtrando automaticamente dados sensíveis em conformidade com a **LGPD** e a **LAI**.

![Banner do Projeto](https://github.com/KD-Devz/Hackathon_Controle_Social_Desafio_Participa_DF/blob/main/static/imagens/Pagina%20Principal%20v2.0.jpeg?raw=true)

🌐 **Acesse agora:** [calebeaf02.pythonanywhere.com](https://calebeaf02.pythonanywhere.com/)

---

## 🚀 O que há de novo na v2.0
Nesta versão, o motor de auditoria evoluiu para um sistema de validação estrita:

* **Validação Matemática Real:** Implementação dos algoritmos de **Módulo 11** e **Luhn** para validar CPF, CNPJ, PIS/PASEP, Título de Eleitor e Cartões de Crédito.
* **Arquitetura Singleton:** Uso da classe `RecursosLinguisticos` para carregamento único de bases na memória RAM, garantindo performance de análise quase instantânea.
* **Análise Semântica Avançada:** Motor `conjugador.py` que detecta intenções em diversos tempos verbais (passado, presente, futuro).
* **Exportação de Relatórios:** Geração de manuais técnicos formais em PDF através da biblioteca `xhtml2pdf`.

---

## 🎯 Diferenciais Tecnológicos
A solução utiliza uma abordagem multicamadas para garantir a precisão:

* **O Maestro (`carregador.py`):** Orquestra a análise dividindo o texto em frases e calculando o score final de criticidade.
* **O Linguista (`conjugador.py`):** Expande verbos no infinitivo para impedir que o sistema seja burlado por variações gramaticais.
* **O Biblioteca (`recursos.py`):** Gerencia listas de referência e nomes do IBGE de forma eficiente em memória.
* **O Higienizador (`texto.py`):** Realiza a limpeza, normalização e validação algorítmica estrita dos documentos.

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
