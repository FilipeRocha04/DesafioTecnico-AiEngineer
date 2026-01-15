import json
from pathlib import Path
from typing import Optional, Dict, Any, List


BASE_DIR = Path(__file__).resolve().parent.parent
MEMORIA_DIR = BASE_DIR / ".memoria"
MEMORIA_DIR.mkdir(parents=True, exist_ok=True)


LIMITE_HISTORICO = 20


def caminho_thread(thread_id: str) -> Path:
    
    if not thread_id:
        raise ValueError("thread_id é obrigatório para criar caminho de memória")
    
    import re

    safe_id = re.sub(r"[^A-Za-z0-9_.-]", "_", thread_id)
    
    if len(safe_id) > 128:
        safe_id = safe_id[:128]
    return MEMORIA_DIR / f"thread_{safe_id}.json"


def _trim_historico(historico: Optional[List[Dict[str, str]]]) -> List[Dict[str, str]]:

    if not historico:
        return []
    if len(historico) <= LIMITE_HISTORICO:
        return historico
 
    return historico[-LIMITE_HISTORICO:]


def salvar_memoria_curta(thread_id: str, estado: Dict[str, Any]) -> None:
   
    if not thread_id:
        return
    caminho = caminho_thread(thread_id)

    
    historico = estado.get("historico")
    estado["historico"] = _trim_historico(historico)


    with caminho.open("w", encoding="utf-8") as f:
        json.dump(estado, f, ensure_ascii=False, indent=2)


def carregar_memoria_curta(thread_id: str) -> Optional[Dict[str, Any]]:
   
    if not thread_id:
        return None
    caminho = caminho_thread(thread_id)
    if not caminho.exists():
        return None
    try:
        with caminho.open("r", encoding="utf-8") as f:
            estado = json.load(f)
          
            estado["historico"] = _trim_historico(estado.get("historico"))
            return estado
    except Exception:
        return None


def adicionar_mensagem(thread_id: str, role: str, texto: str) -> None:
    
    if not thread_id:
        raise ValueError("thread_id é obrigatório para adicionar mensagem")

    estado = carregar_memoria_curta(thread_id) or {"thread_id": thread_id, "historico": []}
    historico = estado.get("historico") or []


    from datetime import datetime
    entrada = {"role": role, "content": texto, "timestamp": datetime.utcnow().isoformat() + "Z"}
    historico.append(entrada)
    estado["historico"] = _trim_historico(historico)

    estado["thread_id"] = thread_id

    salvar_memoria_curta(thread_id, estado)


def obter_historico(thread_id: str) -> List[Dict[str, str]]:
    
    estado = carregar_memoria_curta(thread_id)
    if not estado:
        return []
    return estado.get("historico", [])


def limpar_memoria(thread_id: str) -> None:

    caminho = caminho_thread(thread_id)
    try:
        if caminho.exists():
            caminho.unlink()
    except Exception:
      
        pass
