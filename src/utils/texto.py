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
