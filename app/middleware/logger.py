def _truncate(s: str, limit: int = 400) -> str:
    if not isinstance(s, str):
        s = str(s)
    if len(s) <= limit:
        return s
    return s[:limit].rstrip() + "... (truncated)"


def _format_item(key, value, indent=0, limit=400):
    pad = "  " * indent
    lines = []
    if isinstance(value, dict):
        lines.append(f"{pad}- {key}:")
        for k, v in value.items():
            lines.extend(_format_item(k, v, indent + 1, limit))
    elif isinstance(value, list):
        lines.append(f"{pad}- {key}:")
        for i, v in enumerate(value):
            lines.extend(_format_item(f"[{i}]", v, indent + 1, limit))
    else:
        val = _truncate(value, limit)
        if "\n" in val:
            lines.append(f"{pad}- {key}:")
            for l in val.splitlines():
                lines.append(f"{pad}    {l}")
        else:
            lines.append(f"{pad}- {key}: {val}")
    return lines


def log_evento(etapa: str, dados):
    
    mapa = {
        "openai_chamada": "🤖➜ OpenAI chamada",
        "openai_resposta": "📣 OpenAI resposta",
        "openai_resposta_simulada": "📣 OpenAI (simulada)",
        "validacao": "✅ Validação",
        "orquestrador": "🧭 Orquestrador",
        "decisao_fluxo": "🔀 Decisão de fluxo",
        "calculadora": "🧮 Calculadora",
        "agente_conhecimento": "🤖 Agente de conhecimento",
    }

    titulo = mapa.get(etapa, f"ℹ️ {etapa}")
    print()
    print(titulo)

    if dados is None:
        print("- (sem dados)")
        return

    if isinstance(dados, dict):
        for k, v in dados.items():
            for line in _format_item(k, v, indent=0):
                print(line)
        return

 
    if isinstance(dados, list):
        for i, item in enumerate(dados):
            for line in _format_item(f"[{i}]", item, indent=0):
                print(line)
        return


    for line in _format_item("dados", dados, indent=0):
        print(line)

