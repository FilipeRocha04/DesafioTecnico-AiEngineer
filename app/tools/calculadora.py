import re


def _extrair_expressao(texto: str) -> str:
    
    if not texto:
        return ""

    
    padrao = r"-?\d+(?:\.\d+)?(?:\s*[+\-*/]\s*-?\d+(?:\.\d+)?)*"
    m = re.search(padrao, texto)
    if not m:
        return ""
    return m.group(0)


def calcular(expressao: str) -> str:

    expr = _extrair_expressao(expressao)
    if not expr:
        return "Erro ao calcular: expressão não encontrada"

    expr = expr.replace(',', '.')

    try:
       
        resultado = eval(expr, {"__builtins__": None}, {})
        return str(resultado)
    except Exception:
        return "Erro ao calcular"
