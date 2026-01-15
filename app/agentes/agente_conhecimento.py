from typing import Any
from app.middleware import log_evento
from app.configuracoes import configuracoes

_CHAT_LLM = None
try:
    
    try:
        from langchain.chat_models import ChatOpenAI as _ChatOpenAI
    except Exception:
        from langchain_openai import ChatOpenAI as _ChatOpenAI

    _CHAT_LLM = _ChatOpenAI(
        model=getattr(configuracoes, "OPENAI_MODEL", "gpt-4o-mini"),
        api_key=getattr(configuracoes, "OPENAI_API_KEY", None),
        temperature=getattr(configuracoes, "OPENAI_TEMPERATURE", 0.2),
    )
except Exception:
    _CHAT_LLM = None


class _RespostaSimulada:
    def __init__(self, conteudo: str):
        self.content = conteudo


def _responder_local(pergunta: str):
    
    texto = f"[RESPOSTA SIMULADA] Não há LLM disponível. Pergunta recebida: {pergunta}"
    
    return texto


def responder_conhecimento(pergunta: str):
  
    log_evento("openai_chamada", {"pergunta": pergunta})

    if _CHAT_LLM is None:
        resposta = _responder_local(pergunta)
        log_evento("openai_resposta_simulada", {"conteudo": resposta})
        return resposta

    
    try:
       
        resultado = _CHAT_LLM(pergunta)
        
        if hasattr(resultado, "content"):
            conteudo = resultado.content
        else:
            conteudo = str(resultado)
    except TypeError:
        try:
            resultado = _CHAT_LLM.invoke(pergunta)
            conteudo = getattr(resultado, "content", str(resultado))
        except Exception:
        
            conteudo = _responder_local(pergunta)

   
    if isinstance(conteudo, dict):
        log_evento("openai_resposta", {"conteudo": conteudo.get("resposta"), "acao": conteudo.get("acao")})
        return conteudo

    log_evento("openai_resposta", {"conteudo": conteudo})
    return conteudo