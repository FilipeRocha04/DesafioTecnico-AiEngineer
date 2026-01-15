from app.grafo.estado import EstadoAssistente
from app.agentes.agente_orquestrador import classificar_pergunta
from app.agentes.agente_conhecimento import responder_conhecimento
from app.tools.calculadora import calcular, _extrair_expressao
from app.guardrails.validacoes import validar_entrada
from app.middleware.logger import log_evento
import re


def no_validacao(estado: EstadoAssistente) -> EstadoAssistente:
 
    log_evento("validacao", {"pergunta": estado["pergunta"]})
    validar_entrada(estado["pergunta"])
    return estado


def no_orquestrador(estado: EstadoAssistente) -> EstadoAssistente:
  
    pergunta_raw = estado.get("pergunta", "") or ""
    tipo = classificar_pergunta(pergunta_raw)

    low = pergunta_raw.lower()
    if re.search(r"\d", low) and re.search(r"\b(mais|menos|vezes|dividido por|dividido|x|\bpor\b|/|\+|\-|\*)\b", low):
        tipo = "matematica"

    estado["tipo_pergunta"] = tipo

    log_evento("orquestrador", {"tipo_pergunta": tipo})
    return estado


def no_conhecimento(estado: EstadoAssistente) -> EstadoAssistente:
    
    log_evento("agente_conhecimento", {"pergunta": estado["pergunta"]})

    historico = estado.get("historico") or []
    
    contexto = []
    for item in historico[-10:]:
        role = item.get("role")
        content = item.get("content") or item.get("text") or ""
        contexto.append(f"{role}: {content}")

    
    prompt = "\n".join(contexto + [f"user: {estado.get('pergunta', '')}"])

    resposta = responder_conhecimento(prompt)
    
    if isinstance(resposta, dict):
        
        texto = resposta.get("resposta") or resposta.get("content") or str(resposta)
    else:
        texto = str(resposta)

    estado["resposta"] = texto

    return estado


def no_calculadora(estado: EstadoAssistente) -> EstadoAssistente:
   
    log_evento("calculadora", {"expressao": estado.get("pergunta")})

    pergunta = estado.get("pergunta", "") or ""

   
    norm = pergunta.lower()
   
    norm = norm.replace("mais", "+")
    norm = norm.replace("menos", "-")
    norm = norm.replace("vezes", "*")
    norm = norm.replace(" x ", "*")
    norm = norm.replace("x ", "*")
    norm = norm.replace(" x", "*")
    norm = norm.replace("dividido por", "/")
    norm = norm.replace("dividido", "/")
    
    norm = re.sub(r"[^\d\+\-\*\/\.\(\)\s]", " ", norm)
    
    norm = re.sub(r"\s+", " ", norm).strip()

    
    expressao = _extrair_expressao(norm)

    
    def obter_ultimo_numero_do_assistant(historico_list):
        for item in reversed(historico_list):
            if item.get("role") == "assistant":
                nums = re.findall(r"-?\d+(?:\.\d+)?", str(item.get("content", "")))
                if nums:
                    return nums[-1]
        return None

    historico = estado.get("historico") or []

    
    if expressao and re.match(r"^[\+\-\*/]", expressao.strip()):
        ultimo = obter_ultimo_numero_do_assistant(historico)
        if ultimo is not None:
            expressao = f"{ultimo}{expressao}"
    else:
        
        if expressao and not re.search(r"[\+\-\*/]", expressao) and re.search(r"[\+\-\*/]", norm):
            m = re.search(r"[\+\-\*/]\s*-?\d+(?:\.\d+)?", norm)
            if m:
                operador_expr = m.group(0).replace(" ", "")
                ultimo = obter_ultimo_numero_do_assistant(historico)
                if ultimo is not None:
                    expressao = f"{ultimo}{operador_expr}"

   
    tentativa = expressao or norm or pergunta

    resultado = calcular(tentativa)
    estado["resposta"] = resultado

    return estado
