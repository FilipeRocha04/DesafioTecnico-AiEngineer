# Assistente-IA

Repositório: https://github.com/FilipeRocha04/DesafioTecnico-AiEngineer.git

Projeto de assistente multiagente que orquestra agentes, aplica guardrails para segurança e fornece uma interface de terminal leve para interação.

## Visão geral

O sistema segue uma arquitetura multiagente: um orquestrador classifica as solicitações e faz handoff para agentes especializados. Há uma camada de middleware que intercepta mensagens para logging, métricas e, principalmente, aplicação de guardrails (detecção e tratamento de PII). O histórico de conversas é armazenado localmente para permitir continuidade de contexto entre interações.

## Rápido (Quickstart)

Siga estes passos no Windows PowerShell:

```powershell
git clone https://github.com/FilipeRocha04/DesafioTecnico-AiEngineer.git
cd assistente-ia

# criar e ativar virtualenv (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# instalar dependências
pip install -r requirements.txt


#Crie um arquivo .env com: OPENAI_API_KEY= ''
$env:OPENAI_API_KEY = 'sua_chave_aqui'


# executar
python main.py
```


## Uso

Ao executar, o assistente pedirá por uma pergunta no terminal. Digite sua pergunta e aguarde a resposta — o orquestrador encaminhará para o agente adequado (ex.: tool calculadora para questões matemáticas; agente de conhecimento para respostas baseadas em contexto/LLM).

## Arquitetura (resumo)

- Multiagente: agentes especializados (conhecimento, tool calculadora, etc.) coordenados por um orquestrador.
- Grafo de execução: cada nó representa uma etapa (classificação, processamento, resposta).
- Middleware: interceptadores para logging, métricas e aplicação de guardrails

- Memória: histórico por thread salvo localmente para continuidade de conversa.

## Handoff, Guardrails e Middleware (como estão aplicados)

Handoff
- As transferências entre agentes (handoffs) carregam apenas o contexto mínimo necessário: pergunta, histórico reduzido e identificadores de thread. Antes do handoff, o conteúdo é sanitizado para reduzir exposição de dados sensíveis. Handoffs são registrados com metadados (ids e timestamps) para rastreabilidade.

Guardrails
- Existe uma camada de detecção configurado para bloquear baseado no tamanho da pergunta, o sistema lança uma exceção específica que interrompe o fluxo.

Middleware
- O middleware intercepta mensagens antes de qualquer persistência, log ou chamada externa . 


Boas práticas aplicadas no projeto:
- Aplicar guardrails/middleware antes de qualquer handoff ou persistência.
- Registrar apenas metadados e IDs; se necessário registrar conteúdo, registrar versões redigidas/mascaradas.

## Configuração

- Variáveis importantes:
  - `OPENAI_API_KEY`: chave para chamadas a provedores de LLM.( Nesse projeto usei o modelo gpt-4o-mini)
  - Parâmetros de modelo (nome do modelo, temperatura) podem ser alterados nas configurações do projeto.
- Local de persistência de memória: o sistema salva histórico localmente para permitir continuidade por thread.

## Testes rápidos

1. Rode o assistente e faça uma pergunta  (ex.: "Quanto é 2+2?"), a tool calculadora será acionada se enviar uma pergunta como " Quem foi Silvio Santos?" será acionado o agente de conhecimento.


