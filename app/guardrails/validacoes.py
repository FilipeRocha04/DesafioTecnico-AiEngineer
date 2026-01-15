def validar_entrada(pergunta: str):
    if len(pergunta.strip()) < 2:
        raise ValueError("Pergunta muito curta.")

    if len(pergunta) > 500:
        raise ValueError("Pergunta muito longa.")
