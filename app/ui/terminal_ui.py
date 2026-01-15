import shutil

# Cores ANSI simples
CSI = "\x1b["
RESET = CSI + "0m"
GREEN = CSI + "32m"
CYAN = CSI + "36m"
YELLOW = CSI + "33m"
MAGENTA = CSI + "35m"
WHITE = CSI + "37m"
BOLD = CSI + "1m"


def _print_boxed(text: str, title: str = None, color: str = WHITE) -> None:
    """Imprime um bloco com borda simples e título opcional."""
    # largura do terminal
    width = shutil.get_terminal_size((80, 20)).columns
    lines = text.splitlines() or [""]
    max_line = max(len(line) for line in lines)
    box_width = min(max_line, width - 4)

    # header
    if title:
        header = f" {title} "
        print(color + "┌" + "─" * (len(header)) + "┐" + RESET)
        print(color + "│" + BOLD + header + RESET + color + "│" + RESET)
        print(color + "├" + "─" * (len(header)) + "┤" + RESET)
    else:
        print(color + "┌" + "─" * (box_width + 2) + "┐" + RESET)

    # content
    for line in lines:
        # wrap long lines simply
        if len(line) <= box_width:
            content = line
            padding = box_width - len(content)
            print(color + "│ " + RESET + content + " " * padding + color + " │" + RESET)
        else:
            # naive wrap
            start = 0
            while start < len(line):
                chunk = line[start:start + box_width]
                padding = box_width - len(chunk)
                print(color + "│ " + RESET + chunk + " " * padding + color + " │" + RESET)
                start += box_width

    # footer
    if title:
        print(color + "└" + "─" * (len(header)) + "┘" + RESET)
    else:
        print(color + "└" + "─" * (box_width + 2) + "┘" + RESET)


def mostrar_handoff(origem: str, destino: str) -> None:
    # rótulos amigáveis para agentes
    labels = {
        "orquestrador": "🧭 orquestrador",
        "conhecimento": "🤖 conhecimento",
        "calculadora": "🧮 calculadora",
        "escalacao": "🔁 escalacao",
    }
    rot_origem = labels.get(origem, origem)
    rot_dest = labels.get(destino, destino)
    txt = f"🔀 Handoff: {rot_origem} -> {rot_dest}"
    print(MAGENTA + BOLD + txt + RESET)


def mostrar_agente_ativo(nome: str) -> None:
    labels = {
        "orquestrador": "🧭 orquestrador",
        "conhecimento": "🤖 conhecimento",
        "calculadora": "🧮 calculadora",
        "escalacao": "🔁 escalacao",
    }
    rot = labels.get(nome, nome)
    print(CYAN + BOLD + f"{rot}" + RESET)


def imprimir_usuario(texto: str) -> None:
    # prefixo com emoji para o usuário
    _print_boxed(texto, title="👤 Usuário", color=YELLOW)


def imprimir_assistente(texto: str) -> None:
    _print_boxed(texto, title="🤖 IA (assistant)", color=GREEN)


def imprimir_resposta_formatada(texto: str) -> None:
    """Se o texto contiver marcações como 'user:' e 'assistant:' quebra em vários blocos
    e imprime cada um com o estilo apropriado. Caso contrário, imprime um único bloco
    de assistant como antes.
    """
    import re

    if not texto or not isinstance(texto, str):
        imprimir_assistente(str(texto))
        return

    # detectar padrões tipo 'user: ...' e 'assistant: ...' (case-insensitive)
    pattern = re.compile(r"(?i)(user|assistant):\s*(.*?)(?=(?:\n(?:user|assistant):)|\Z)", re.S)
    matches = list(pattern.finditer(texto))

    if not matches:
        # texto normal
        imprimir_assistente(texto)
        return

    # imprimir cada segmento conforme o role
    for m in matches:
        role = m.group(1).lower()
        content = m.group(2).strip()
        if role == "user":
            imprimir_usuario(content)
        else:
            imprimir_assistente(content)


def imprimir_info(texto: str) -> None:
    print(WHITE + texto + RESET)
