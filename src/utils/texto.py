import re

import unicodedata


def normalizar_ao_retirar_acentuacao_e_cedilha(texto: str) -> str:
    nfkd = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join([c for c in nfkd if not unicodedata.combining(c)])
    sem_acento = sem_acento.replace("ç", "c").replace("Ç", "C")
    return sem_acento.upper()


def limpar_texto(texto: str) -> str:
    apenas_letras_numeros = re.sub(r'[^A-Za-z0-9 ]+', ' ', texto)
    return apenas_letras_numeros.upper()


def validar_cpf_math(cpf):
    """Aplica o algoritmo de Módulo 11 para validar CPF real."""
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(i))
        digito = (soma * 10 % 11) % 10
        if digito != int(cpf[i]):
            return False
    return True


def validar_cnpj_math(cnpj):
    """Aplica o algoritmo de Módulo 11 para validar CNPJ real."""
    cnpj = ''.join(filter(str.isdigit, cnpj))
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False

    def calcular_digito(payload, pesos):
        soma = sum(int(a) * b for a, b in zip(payload, pesos))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    d1 = calcular_digito(cnpj[:12], pesos1)
    d2 = calcular_digito(cnpj[:12] + d1, pesos2)

    return cnpj[-2:] == d1 + d2


def validar_pis_math(pis):
    """Valida PIS/PASEP usando Módulo 11."""
    pis = ''.join(filter(str.isdigit, pis))
    if len(pis) != 11 or pis == pis[0] * 11:
        return False

    pesos = [3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(pis[i]) * pesos[i] for i in range(10))

    resto = soma % 11
    digito = 0 if resto < 2 else 11 - resto

    return int(pis[10]) == digito


def validar_cartao_math(n_cartao):
    """Aplica o Algoritmo de Luhn para validar cartões de crédito."""
    n_cartao = ''.join(filter(str.isdigit, n_cartao))
    if not n_cartao: return False

    r = [int(ch) for ch in n_cartao][::-1]
    soma = sum(r[0::2]) + sum(sum(divmod(d * 2, 10)) for d in r[1::2])

    return soma % 10 == 0


def validar_titulo_eleitor_math(titulo):
    """Valida Título de Eleitor (Dígitos verificadores e UF)."""
    titulo = ''.join(filter(str.isdigit, titulo)).zfill(12)
    if len(titulo) != 12: return False

    # Validação do primeiro dígito (9 primeiros números)
    pesos1 = list(range(2, 11))
    soma1 = sum(int(titulo[i]) * pesos1[i] for i in range(8))
    d1 = soma1 % 11
    d1 = 0 if d1 == 10 else d1

    # Validação do segundo dígito (D1 + Código UF)
    pesos2 = [7, 8, 9]  # Pesos para os dígitos 9, 10 e D1
    soma2 = sum(int(titulo[i]) * pesos2[i - 9] for i in range(9, 11)) + (d1 * 9)
    d2 = soma2 % 11
    d2 = 0 if d2 == 10 else d2

    return int(titulo[10]) == d1 and int(titulo[11]) == d2

def avaliar_documentos(texto):
    score_extra = 0
    # Exemplo: se achar um padrão que parece cartão E a matemática bater
    if validar_cartao_math(texto):
        score_extra += 0.8  # Risco altíssimo
    if validar_pis_math(texto):
        score_extra += 0.5  # Risco moderado/alto
    return score_extra