import re
from app.tools.calculadora import calcular
from app.agentes.agente_conhecimento import responder_conhecimento
from app.middleware import interceptar_execucao


def classificar_pergunta(pergunta: str) -> str:
    
    texto = pergunta.lower() if pergunta else ""

    
    termos_conhecimento = [
        "ano", "anos", "idade", "nasci", "nascimento", "quantos anos", "tenho", "nasci em",
        "data de nascimento",
    ]
    for termo in termos_conhecimento:
        if termo in texto:
            return "conhecimento"

    
    padrao_expr = re.compile(r"^-?\d+(?:\.\d+)?(?:\s*[+\-*/]\s*-?\d+(?:\.\d+)?)+$")
    if padrao_expr.search(texto.strip()):
        return "matematica"

    if any(op in pergunta for op in ["+", "-", "*", "/"]) or any(w in texto for w in ["calcule", "quanto é", "quanto e", "resultado"]):
        return "matematica"

    return "conhecimento"


def processar_pergunta(pergunta: str) -> str:

    interceptar_execucao("entrada_usuario", {"pergunta": pergunta})

    tipo = classificar_pergunta(pergunta)
    if tipo == "matematica":
        interceptar_execucao("roteamento", {"destino": "calculadora"})
        return calcular(pergunta)

    interceptar_execucao("roteamento", {"destino": "conhecimento"})
    return responder_conhecimento(pergunta)

