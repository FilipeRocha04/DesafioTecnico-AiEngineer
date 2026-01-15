# Assistente-IA

Repositório: https://github.com/FilipeRocha04/DesafioTecnico-AiEngineer.git

Projeto de assistente multiagente que orquestra agentes, aplica guardrails para segurança e fornece uma interface de terminal leve para interação.

## Visão geral

O sistema segue uma arquitetura multiagente: um orquestrador classifica as solicitações e faz handoff para agentes especializados. Há uma camada de middleware que intercepta mensagens para logging, métricas e, principalmente, aplicação de guardrails (detecção e tratamento de PII). O histórico de conversas é armazenado localmente para permitir continuidade de contexto entre interações.

# (Quickstart)

Siga estes passos no Windows PowerShell:

```powershell
git clone https://github.com/FilipeRocha04/DesafioTecnico-AiEngineer.git
cd DesafioTecnico-AiEngineer

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
- Guardrails/middleware antes de qualquer handoff ou persistência.
## Configuração

- Variáveis importantes:
  - `OPENAI_API_KEY`: chave para chamadas a provedores de LLM.( Nesse projeto usei o modelo gpt-4o-mini)
  - Parâmetros de modelo (nome do modelo, temperatura) podem ser alterados nas configurações do projeto.
- Local de persistência de memória: o sistema salva histórico localmente para permitir continuidade por thread.

## Testes rápidos

1. Rode o assistente e faça uma pergunta  (ex.: "Quanto é 2+2?"), a tool calculadora será acionada se enviar uma pergunta como " Quem foi Silvio Santos?" será acionado o agente de conhecimento.


 ## QUAL FOI SUA LÓGICA DE IMPLEMENTAÇÃO:
Optei por desenvolver o desafio utilizando LangGraph em vez de LangChain porque o objetivo do teste era demonstrar clareza de raciocínio. O LangGraph me permitiu modelar explicitamente o comportamento do assistente como um fluxo de estados bem definido, deixando claro onde a decisão é tomada, quando um agente é acionado e como a resposta retorna ao usuário. Para um desafio técnico que avalia lógica e organização, essa abordagem torna o raciocínio muito mais transparente do que uma cadeia implícita de chamadas.
Ao usar LangGraph, cada etapa do sistema foi pensada como um nó do grafo: primeiro a validação da entrada, depois a classificação da pergunta, seguida do encaminhamento para o agente adequado (handoff) e, por fim, a geração da resposta. Isso torna explícito o “quando” e o “porquê” de cada decisão, exatamente um dos pontos avaliados no desafio, que pede clareza na lógica de decisão entre responder com o modelo ou acionar uma ferramenta externa 
A arquitetura foi desenhada como um sistema multiagente, com um orquestrador central responsável apenas por coordenar o fluxo. Esse orquestrador não responde perguntas diretamente; ele analisa a solicitação do usuário e decide se deve transferir o controle para um agente de conhecimento (LLM) ou para uma tool específica, como a calculadora. Essa separação reforça o princípio de responsabilidade única e evita acoplamento entre decisão e execução.
Antes de qualquer handoff ou persistência, as mensagens passam por uma camada de middleware, que intercepta o fluxo para aplicar logging, métricas e principalmente guardrails. Esses guardrails funcionam como um mecanismo de proteção: por exemplo, validações de tamanho de entrada podem interromper imediatamente o fluxo lançando exceções específicas, garantindo que nenhuma chamada externa ou gravação de histórico aconteça sem validação prévia. Isso demonstra preocupação com segurança e previsibilidade, mesmo em um sistema simples.
Os handoffs entre agentes foram implementados de forma controlada, carregando apenas o contexto mínimo necessário — pergunta, histórico reduzido e identificadores de thread. Antes da transferência, o conteúdo é sanitizado para reduzir exposição de dados sensíveis, e metadados como IDs e timestamps são registrados para rastreabilidade. Dessa forma, o handoff deixa de ser apenas uma troca de função e passa a ser uma transição explícita de responsabilidade dentro do fluxo.
Por fim, a memória do sistema é mantida de forma simples e local, organizada por thread, permitindo continuidade de contexto entre interações sem introduzir complexidade desnecessária. A escolha por uma interface de terminal (CLI) também foi intencional: ela reduz distrações de interface gráfica e mantém o foco no que o desafio realmente avalia — lógica de decisão, organização do código, integração com LLMs e uso consciente de ferramentas externas.
Em resumo, a escolha do LangGraph foi estratégica para mostrar, de forma clara e técnica, como penso e estruturo sistemas de IA: fluxos explícitos, decisões rastreáveis, agentes bem delimitados e segurança aplicada antes da execução, alinhando diretamente a implementação aos critérios do desafio técnico.





 ## O QUE VOCÊ APRENDEU
Ao desenvolver este desafio, o principal aprendizado foi entender que construir um assistente de IA não se resume a gerar respostas corretas, mas envolve controlar decisões, fluxo e responsabilidade ao longo de toda a execução. A implementação reforçou a importância de orquestrar agentes de forma explícita, aplicar validações antes de qualquer processamento e tratar ferramentas externas como componentes críticos do sistema, e não apenas como atalhos para o modelo de linguagem. Também ficou evidente como a aplicação de guardrails e middleware desde o início aumenta significativamente a confiabilidade do sistema, impedindo que dados inválidos ou sensíveis avancem no fluxo. Mesmo em um projeto simples, priorizar controle e segurança resulta em uma arquitetura mais previsível, organizada e fácil de evoluir.

## O QUE FARIA DIFERENTE COM MAIS TEMPO:
Com mais tempo, eu integraria o Tavily para permitir buscas externas em tempo real, tornando o agente capaz de reconhecer quando o conhecimento interno do modelo não é suficiente e complementar suas respostas com informações atualizadas. Isso elevaria a qualidade das respostas e tornaria o assistente mais útil em cenários reais. Além disso, eu avançaria na tomada de decisão do sistema, substituindo regras simples por uma classificação de intenção mais precisa para o uso de ferramentas. Também estruturaria melhor a memória, separando contexto imediato de conhecimento reutilizável, evitando acúmulo desnecessário de histórico.
Por fim, eu adicionaria maior observabilidade ao sistema, integrando ferramentas como o LangSmith para acompanhar custo, latência, traces de execução e comportamento dos agentes ao longo do fluxo. Isso facilitaria debugging, ajustes finos e avaliação do desempenho do sistema. Em conjunto, também implementaria estratégias de fallback para garantir resiliência caso ferramentas ou modelos não estejam disponíveis. Essas melhorias manteriam a simplicidade do projeto, mas o aproximariam de um ambiente de produção, sem comprometer a clareza arquitetural.








