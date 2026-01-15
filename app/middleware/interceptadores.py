from .logger import log_evento


def interceptar_execucao(etapa: str, dados: dict):

    try:
        log_evento(etapa, dados)
    except Exception:
 
        pass
