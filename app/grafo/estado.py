from typing import TypedDict, Optional, List, Dict


class EstadoAssistente(TypedDict, total=False):

    pergunta: str
    resposta: str
    tipo_pergunta: Optional[str]
    rota: Optional[str]
    thread_id: Optional[str]
    historico: Optional[List[Dict[str, str]]]
