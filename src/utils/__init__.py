from src.utils.carregador import (
    processar_testes,
    processar_index,
    termos_sensiveis,
    variacoes_verbos,
    palavras_interrogativas
)

from src.utils.banco import (
    inicializar_banco,
    registrar_palavra_proibida
)

from src.utils.conjugador import (
    remover_acentos,
    carregar_verbos,
    gerar_variacoes_verbo_regular,
    carregar_verbos_irregulares,
    gerar_lista_variacoes
)

from src.utils.texto import (
    normalizar_ao_retirar_acentuacao_e_cedilha,
    limpar_texto,
)
