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
