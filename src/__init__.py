from .banco import (
    inicializar_banco,
    registrar_palavra_proibida
)
from .carregador import processar_index, processar_testes

from .conjugador import (
    remover_acentos,
    carregar_verbos,
    gerar_variacoes_verbo_regular,
    carregar_verbos_irregulares,
    gerar_lista_variacoes
)

from .texto import (
    normalizar_ao_retirar_acentuacao_e_cedilha,
    limpar_texto,
)

from .paginas import (
    index_bp,
    testes_bp,
    ranking_bp,
    testes_detalhados_bp,
    perfil_bp,
    auth_bp,
    enviar_solicitacao_bp
)
