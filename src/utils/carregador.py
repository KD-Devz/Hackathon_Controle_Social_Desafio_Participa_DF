import csv
import re

from src.utils.texto import (
    limpar_texto,
)
from src.utils.texto import normalizar_ao_retirar_acentuacao_e_cedilha
from utils.recursos import RecursosLinguisticos


# Variáveis globais que podem ser importadas em outros módulos

def contem_padrao(palavras, padrao):
    padrao_lista = padrao.split()  # quebra em palavras
    n, m = len(palavras), len(padrao_lista)

    for i in range(n - m + 1):
        if palavras[i:i + m] == padrao_lista:
            return True
    return False


def processar_index(mensagem: str):
    recursos = RecursosLinguisticos()

    contCriticidade = 0
    contLinearidade = 0
    contIdentificadores = 0
    contExigencias = 0  # Inicializado aqui

    linhas_por_barra_n = mensagem.split('\n')
    linhas_padroes = [linha.strip() for linha in linhas_por_barra_n if linha.strip()]
    nomes_completos_encontrados = set()

    # Inicialização do dicionário com os padrões de auditoria
    padroes_encontrados = {
        "CPF": [],
        "CNPJ": [],
        "RG": [],
        "CEP": [],
        "NOME": [],
        "PROCESSO": [],
        "TITULO_ELEITOR": [],  # Adicionado
        "CNH": [],  # Adicionado
        "PIS_PASEP": [],
        "TELEFONE": [],
        "EMAIL": []
    }

    termos_sensiveis_unicos = set()
    nomes_completos_geral = set()

    # Primeira passada: Detectar padrões globais
    for linha in linhas_padroes:
        achados = validar_padroes_sensiveis(linha)
        for chave in padroes_encontrados:
            if chave in achados:
                padroes_encontrados[chave].extend(achados[chave])

    linhas = [linha.strip() for linha in mensagem.split('.') if linha.strip()]
    resultado_linhas = []
    status_global = "False"

    for linha in linhas:
        linha_normalizada = normalizar_ao_retirar_acentuacao_e_cedilha(linha)
        linha_normalizada = limpar_texto(linha_normalizada)
        palavras = linha_normalizada.split()

        # Detecção de nomes na linha
        nomes_na_linha_atual = set()
        nomes_detectados = obter_nomes(palavras)
        for nc in nomes_detectados:
            nomes_na_linha_atual.add(nc)
            nomes_completos_geral.add(nc)
            nomes_completos_encontrados.add(nc)

        nomes_linha_unicos = remover_substrings(nomes_na_linha_atual)

        # Detecção de termos sensíveis da lista de recursos
        termos_sensiveis_encontrados = []
        for termo in recursos.termos_sensiveis:
            if contem_padrao(palavras, termo):
                termos_sensiveis_unicos.add(termo)
                termos_sensiveis_encontrados.append(termo)

        # Detecção de padrões regex (CPF, Processo, etc) na linha atual
        padroes_na_linha = validar_padroes_sensiveis(linha)
        tem_padrao_regex = any(len(v) > 0 for k, v in padroes_na_linha.items() if k != "NOME")

        # Verbos e Interrogativas
        verbos_encontrados = list(
            set([infinitivo for forma, infinitivo in recursos.variacoes_verbos if forma in linha_normalizada]))
        interrogativas_encontradas = [p for p in recursos.palavras_interrogativas if p in palavras]

        # --- Lógica de Validação Estrita ---

        # Verificamos se há algum risco identificado (Dado Sensível ou Padrão de Documento)
        tem_risco_na_linha = (len(termos_sensiveis_encontrados) > 0 or
                              len(nomes_linha_unicos) > 0 or
                              tem_padrao_regex)

        # Uma solicitação só é INVÁLIDA (True) se houver:
        # (Risco E Verbo) OU (Risco E Interrogação)
        if tem_risco_na_linha and (verbos_encontrados or interrogativas_encontradas):
            status = "True"  # Linha Inválida / Sensível
            status_global = "True"
            contLinearidade += 1
        else:
            status = "False"  # Linha Válida / Segura

        resultado_linhas.append({
            "texto": linha,
            "status": status,
            "termos_sensiveis_encontrados": termos_sensiveis_encontrados,
            "interrogativas": interrogativas_encontradas,
            "verbos": verbos_encontrados,
            "nomes": list(nomes_linha_unicos)
        })

    # Finalização dos Identificadores
    lista_de_nomes_completos_unicos = remover_substrings(nomes_completos_encontrados)
    for nome_encontrado in lista_de_nomes_completos_unicos:
        if nome_encontrado not in padroes_encontrados["NOME"]:
            padroes_encontrados["NOME"].append(nome_encontrado)

    for item in padroes_encontrados.values():
        contIdentificadores += len(item)

    # Cálculo da Criticidade
    contCriticidade = contLinearidade * len(termos_sensiveis_unicos) * contIdentificadores
    valor_norm, adjetivo = calcular_escala_criticidade(contCriticidade)

    return {

        "STATUS": status_global,
        "MENSAGEM": mensagem,
        "linhas": resultado_linhas,
        "PADROES": padroes_encontrados,
        "NOME": lista_de_nomes_completos_unicos,
        "CRITICIDADE": contCriticidade,
        "CRITICIDADE_NORM": round(valor_norm, 2),
        "ADJETIVO": adjetivo,
        "LINEARIDADE": contLinearidade,
        "IDENTIFICADORES": contIdentificadores,
        "EXIGENCIAS": contExigencias
    }


def processar_testes(caminho_csv: str):
    linhas = []
    with open(caminho_csv, newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            linhas.append(row)

    cabecalho = linhas[0]
    dados = linhas[1:]

    resultado_dados = []
    total_validos = 0
    total_invalidos = 0

    for row in dados:
        # Junta os campos da linha em um único texto
        linha_texto = " ".join(row)

        # 🔹 Usa diretamente a função processar_index
        resultado = processar_index(linha_texto)

        # Se STATUS == "True" → inválido
        if resultado["STATUS"] == "True":
            status = "Inválido"
            total_invalidos += 1
        else:
            status = "Válido"
            total_validos += 1

        resultado_dados.append({
            "campos": row,
            "status": status,
            "detalhes": resultado["linhas"]  # mantém os detalhes da análise
        })

    total_testes = len(dados)

    return {
        "cabecalho": cabecalho,
        "dados": resultado_dados,
        "total_testes": total_testes,
        "total_validos": total_validos,
        "total_invalidos": total_invalidos
    }


def validar_padroes_sensiveis(texto):
    """
    Analisa o texto em busca de padrões de dados sensíveis (LGPD)
    para auditoria de solicitações.
    """

    # 1. Inicialização do dicionário de resultados
    resultados = {
        "CPF": [],
        "CNPJ": [],
        "RG": [],
        "CEP": [],
        "NOME": [],
        "PROCESSO": [],
        "TITULO_ELEITOR": [],
        "CNH": [],
        "PIS_PASEP": [],
        "TELEFONE": [],
        "EMAIL": []
    }

    # 2. Definição dos Padrões Regex
    # --- Documentos Civis ---
    padrao_cpf = r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b'
    padrao_cnpj = r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b'
    padrao_rg = r'\b\d{1,2}\.?\d{3}\.?\d{3}-?[\dX]\b|\b\d{5,13}\b'
    padrao_titulo = r'\b\d{12}\b'
    padrao_cnh = r'\b\d{11}\b'
    padrao_pis = r'\b\d{3}\.\d{5}\.\d{2}\.\d{1}\b'

    # --- Contato e Localização ---
    padrao_cep = r'\b\d{5}-?\d{3}\b'
    padrao_tel = r'\(?\d{2}\)?\s?9?\d{4}-?\d{4}'
    padrao_email = r'[\w\.-]+@[\w\.-]+\.\w+'

    # --- Judiciário/Administrativo ---
    # Padrão: 0000-000000000/0000-00 (Ex: SEI/GDF)
    padrao_processo = r'\b\d{4,5}-\d{7,9}/\d{4}-\d{2}\b'

    # 3. Execução das Buscas (FindAll)
    # Importante: As chaves aqui devem ser idênticas às do dicionário inicial
    resultados["CPF"] = re.findall(padrao_cpf, texto)
    resultados["CNPJ"] = re.findall(padrao_cnpj, texto)
    resultados["RG"] = re.findall(padrao_rg, texto)
    resultados["CEP"] = re.findall(padrao_cep, texto)
    resultados["PROCESSO"] = re.findall(padrao_processo, texto)
    resultados["TITULO_ELEITOR"] = re.findall(padrao_titulo, texto)
    resultados["CNH"] = re.findall(padrao_cnh, texto)
    resultados["PIS_PASEP"] = re.findall(padrao_pis, texto)
    resultados["TELEFONE"] = re.findall(padrao_tel, texto)
    resultados["EMAIL"] = re.findall(padrao_email, texto)

    return resultados


def obter_nomes(palavras):
    recursos = RecursosLinguisticos()

    nome_completo = ""
    tem_nome = False
    tem_sobrenome = False
    tem_nome_ou_sobrenome = False

    nomes_completos_encontrados = set()
    for palavra in palavras:
        includo = False
        tem_nome_ou_sobrenome = False

        if palavra in recursos.nomes:
            tem_nome = True
            tem_nome_ou_sobrenome = True
            includo = True

        if palavra in recursos.sobrenomes:
            tem_sobrenome = True
            tem_nome_ou_sobrenome = True
            includo = True

        if includo:
            nome_completo = nome_completo + " " + palavra

        if tem_nome_ou_sobrenome == False and len(nome_completo.strip()) > 0:
            nomes_completos_encontrados.add(nome_completo.strip())
            nome_completo = ""

    if tem_nome_ou_sobrenome == False:
        if len(nome_completo.strip()) > 0:
            nomes_completos_encontrados.add(nome_completo.strip())
            nome_completo = ""

    if len(nome_completo.strip()) > 0:
        nomes_completos_encontrados.add(nome_completo.strip())
        nome_completo = ""

    return nomes_completos_encontrados


def remover_substrings(lista):
    resultado = []
    for item in lista:
        # Verifica se o item está contido em algum outro item da lista
        if not any(item != outro and item in outro for outro in lista):
            resultado.append(item)
    return resultado


def calcular_escala_criticidade(valor_bruto):
    # Definimos um valor máximo teórico para o sistema (ex: 1000)
    # ou usamos o maior valor observado na amostra atual
    valor_max = 1000
    valor_min = 0

    # Aplicação da fórmula de normalização
    normalizado = (valor_bruto - valor_min) / (valor_max - valor_min)

    # Garantir que o índice fique entre 0 e 1
    normalizado = max(0, min(1, normalizado))

    # Atribuição do adjetivo com base na sua escala
    if normalizado <= 0.20:
        return normalizado, "Crítico Leve (Alarmante)"
    elif normalizado <= 0.40:
        return normalizado, "Crítico Moderado (Perigoso)"
    elif normalizado <= 0.60:
        return normalizado, "Crítico Elevado (Grave)"
    elif normalizado <= 0.80:
        return normalizado, "Crítico Severo (Severo)"
    else:
        return normalizado, "Crítico Extremo (Catastrófico)"
