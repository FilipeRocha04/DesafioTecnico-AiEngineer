from app.grafo.fluxo import criar_grafo
from app.guardrails.validacoes import validar_entrada
from app.memoria.memoria_curta import (
    carregar_memoria_curta,
    salvar_memoria_curta,
    adicionar_mensagem,
)
from app.ui.terminal_ui import (
    imprimir_usuario,
    imprimir_assistente,
    mostrar_agente_ativo,
    mostrar_handoff,
)


def main():
    grafo = criar_grafo()

    
    print("Bem-vindo ao Assistente IA 🤖")
    
    thread_id = "1"
    # print("Usando thread persistente padrão: '1'\n")

    print("Digite 'sair' para encerrar a sessão")

    agente_ativo_anterior = None


    estado_corrente = {}
    if thread_id:
        salvo = carregar_memoria_curta(thread_id)
        if salvo:
            estado_corrente = salvo

    while True:
        pergunta = input("Pergunta: ")
        if pergunta.lower().strip() in ("sair", "exit", "quit"):
            print("Encerrando...")
            break

        try:
            
            validar_entrada(pergunta)

           
            estado = estado_corrente
            estado["pergunta"] = pergunta
            estado["thread_id"] = thread_id
            estado.setdefault("historico", [])

           
            estado["historico"].append({"role": "user", "content": pergunta})
            if thread_id:
                try:
                    adicionar_mensagem(thread_id, "user", pergunta)
                except Exception:
                   
                    pass

           
            imprimir_usuario(pergunta)

            resultado = grafo.invoke(estado)

            
            rota = resultado.get("rota") or resultado.get("tipo_pergunta")
            agente_ativo = None
            if rota:
            
                if rota == "calculadora" or rota == "matematica":
                    agente_ativo = "calculadora"
                elif rota == "conhecimento":
                    agente_ativo = "conhecimento"
                elif rota == "escalacao":
                    agente_ativo = "escalacao"

            
            if agente_ativo and agente_ativo != agente_ativo_anterior:
                
                origem = agente_ativo_anterior or "orquestrador"
                mostrar_handoff(origem, agente_ativo)
                mostrar_agente_ativo(agente_ativo)
                agente_ativo_anterior = agente_ativo

            
            resposta = resultado.get("resposta")
            if resposta:
       
                try:
                    from app.ui.terminal_ui import imprimir_resposta_formatada

                    if isinstance(resposta, str):
                        imprimir_resposta_formatada(resposta)
                    else:
                        imprimir_assistente(str(resposta))
                except Exception:
                    imprimir_assistente(str(resposta))

                
                resultado.setdefault("historico", [])

                ultimo_assistente = None
                if isinstance(resposta, str):
                    import re
                    pattern = re.compile(r"(?i)assistant:\s*(.*?)(?=(?:\n(?:user|assistant):)|\Z)", re.S)
                    matches = list(pattern.finditer(resposta))
                    if matches:
                        ultimo_assistente = matches[-1].group(1).strip()
                if ultimo_assistente is None:
                    ultimo_assistente = str(resposta)

            
                resultado["historico"].append({"role": "assistant", "content": ultimo_assistente})

        
                if thread_id:
                    try:
                        adicionar_mensagem(thread_id, "assistant", ultimo_assistente)
                    except Exception:
                        pass

            # atualizar estado corrente para o próximo turno
            estado_corrente = resultado

            # salvar apenas se houver thread_id (persistência entre execuções)
            if thread_id:
                salvar_memoria_curta(thread_id, resultado)

        except ValueError as e:
            print(f"[ERRO DE VALIDAÇÃO] {e}")


if __name__ == "__main__":
    main()
