from langgraph.graph import StateGraph, END

from app.grafo.estado import EstadoAssistente
from app.grafo.nos import (
    no_validacao,
    no_orquestrador,
    no_conhecimento,
    no_calculadora,
)
from app.middleware.logger import log_evento


def criar_fluxo():
    grafo = StateGraph(EstadoAssistente)

    grafo.add_node("validacao", no_validacao)
    grafo.add_node("orquestrador", no_orquestrador)
    grafo.add_node("conhecimento", no_conhecimento)
    grafo.add_node("calculadora", no_calculadora)

    grafo.set_entry_point("validacao")
    grafo.add_edge("validacao", "orquestrador")

    def decidir_proximo_passo(estado: EstadoAssistente) -> str:
        tipo = estado.get("tipo_pergunta")

        log_evento(
            "decisao_fluxo",
            {"tipo_pergunta": tipo}
        )

        if tipo == "matematica":
            return "calculadora"
        return "conhecimento"

    grafo.add_conditional_edges(
        "orquestrador",
        decidir_proximo_passo,
        {
            "calculadora": "calculadora",
            "conhecimento": "conhecimento",
        },
    )

    grafo.add_edge("calculadora", END)
    grafo.add_edge("conhecimento", END)

    return grafo.compile()



def criar_grafo():
 
    return criar_fluxo()
