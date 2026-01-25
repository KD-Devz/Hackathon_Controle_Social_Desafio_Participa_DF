import csv
import re

from src.utils.banco import registrar_palavra_proibida
from src.utils.conjugador import gerar_lista_variacoes
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

    linhas_por_barra_n = mensagem.split('\n')
    linhas_padroes = [linha.strip() for linha in linhas_por_barra_n if linha.strip()]

    nomes_completos_encontrados = set()


    for linha in linhas_por_barra_n:
        for nome_completo in obter_nomes([normalizar_ao_retirar_acentuacao_e_cedilha(l.upper()) for l in linha.split(' ')]):
            nomes_completos_encontrados.add(nome_completo)

    padroes_encontrados = {"CPF": [], "CNPJ": [], "RG": [], "CEP": [],"NOMES":[]}

    termos_sensiveis_unicos = set()
    nomes_na_solicitacao = set()
    sobrenomes_na_solicitacao = set()
    nomes_completos_geral = set()


    for linha in linhas_padroes:
        achados = validar_padroes_sensiveis(linha)
        for chave in padroes_encontrados:
            padroes_encontrados[chave].extend(achados[chave])

    linhas = [linha.strip() for linha in mensagem.split('.') if linha.strip()]
    resultado_linhas = []
    status_global = "False"





    for linha in linhas:
        linha_normalizada = normalizar_ao_retirar_acentuacao_e_cedilha(linha)
        linha_normalizada = limpar_texto(linha_normalizada)
        palavras = linha_normalizada.split()

        # --- AQUI ESTÁ A MUDANÇA ---
        # 2. Criamos um set temporário apenas para esta linha específica
        nomes_na_linha_atual = set()

        # 3. Detectamos nomes completos APENAS nesta linha
        nomes_detectados = obter_nomes(palavras)
        for nc in nomes_detectados:
            nomes_na_linha_atual.add(nc)
            nomes_completos_geral.add(nc)  # Adiciona ao geral também

        # 4. Limpamos substrings (ex: evitar "João" e "João Silva" na mesma linha)
        nomes_linha_unicos = remover_substrings(nomes_na_linha_atual)
        # ---------------------------

        for nome_completo in obter_nomes(palavras):
            nomes_completos_encontrados.add(nome_completo)

        nomes_na_linha = [p for p in palavras if p in recursos.nomes]
        for nome in nomes_na_linha:
            nomes_na_solicitacao.add(nome)

        sobrenomes_na_linha = [p for p in palavras if p in recursos.sobrenomes]
        for sobrenome in sobrenomes_na_linha:
            sobrenomes_na_solicitacao.add(sobrenome)

        termos_sensiveis_encontrados = []

        for termo in recursos.termos_sensiveis:
            if contem_padrao(palavras, termo):
                registrar_palavra_proibida(termo)
                termos_sensiveis_unicos.add(termo)
                termos_sensiveis_encontrados.append(termo)
                print("Termo sensivel encontrado : ", termo)

        print("------------ SENSIVEIS ------------------")
        print(termos_sensiveis_encontrados)

        verbos_encontrados = [infinitivo for forma, infinitivo in recursos.variacoes_verbos if forma in linha_normalizada]
        interrogativas_encontradas = [p for p in recursos.palavras_interrogativas if p in palavras]

        if (len(termos_sensiveis_encontrados) > 0 and verbos_encontrados) or (
                len(termos_sensiveis_encontrados) > 0 and interrogativas_encontradas):
            status = "True"
            status_global = "True"
            contLinearidade += 1
        else:
            status = "False"

        lista_de_nomes_completos_unicos = remover_substrings(nomes_completos_encontrados)

        resultado_linhas.append({
            "texto": linha,
            "status": status,
            "termos_sensiveis_encontrados": termos_sensiveis_encontrados,
            "interrogativas": interrogativas_encontradas,
            "verbos": list(set(verbos_encontrados)),
            "nomes": list(nomes_linha_unicos)
        })

    lista_de_nomes_completos_unicos = remover_substrings(nomes_completos_encontrados)

    for nome_encontrado in lista_de_nomes_completos_unicos:
        padroes_encontrados["NOMES"].append(nome_encontrado)

    for item in padroes_encontrados.values():
        contIdentificadores += len(item)

    contCriticidade = contLinearidade * len(termos_sensiveis_unicos)*contIdentificadores

    if contCriticidade > 0:
        status_global = "True"

    print("------------ NOMES ------------------")
    print(nomes_na_solicitacao)
    print("------------ SOBRENOMES ------------------")
    print(sobrenomes_na_solicitacao)
    print("------------ NOMES COMPLETOS ------------------")
    print(nomes_completos_encontrados)
    print("------------ NOMES COMPLETOS Unicos ------------------")
    print(lista_de_nomes_completos_unicos)

    print("------------ INTERROGATIVAS ENCONTRADAS ------------------")
    print(recursos.palavras_interrogativas)

    print("------------ PADROES ------------------")
    print(padroes_encontrados)
    print("----------------------------------------")




    return {"STATUS": status_global, "MENSAGEM": mensagem, "linhas": resultado_linhas, "PADROES": padroes_encontrados, "NOMES": lista_de_nomes_completos_unicos,
            "CRITICIDADE": contCriticidade, "LINEARIDADE": contLinearidade, "IDENTIFICADORES": contIdentificadores}


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
    resultados = {
        "CPFS": [],
        "CNPJS": [],
        "RGS": [],
        "CEPS": [],
        "NOMES":[]
    }

    # CPF: 000.000.000-00 ou 00000000000
    padrao_cpf = r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b'

    # CNPJ: 00.000.000/0000-00 ou 00000000000000
    padrao_cnpj = r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b'

    # RG (Padrão variado, mas focado em sequências numéricas comuns de 7 a 9 dígitos)
    padrao_rg = r'\b\d{1,2}\.?\d{3}\.?\d{3}-?[\dX]\b'

    # CEP: 00000-000 ou 00000000
    padrao_cep = r'\b\d{5}-?\d{3}\b'

    resultados["CPF"] = re.findall(padrao_cpf, texto)
    resultados["CNPJ"] = re.findall(padrao_cnpj, texto)
    resultados["RG"] = re.findall(padrao_rg, texto)
    resultados["CEP"] = re.findall(padrao_cep, texto)

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
            nome_completo=""

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
