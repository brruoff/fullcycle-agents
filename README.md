# Operador de Conta — Agente IA com Google ADK

Agente conversacional de atendimento ao cliente construído com [Google ADK](https://google.github.io/adk-docs/), desenvolvido durante o curso **FullCycle**.

## O que faz

- Informa status e detalhes da assinatura do cliente
- Lista e tira dúvidas sobre faturas
- Processa solicitações de cancelamento
- Usa Gemini como modelo de linguagem

## Stack

| Componente | Versão                |
|---|-----------------------|
| Python | 3.12                  |
| google-adk | 2.2.0                 |
| Gemini | gemini-3.1-flash-lite |

## Setup

```bash
# instalar dependências
uv sync

# configurar variável de ambiente
cp .env.example .env
# edite .env e adicione sua GOOGLE_API_KEY
```

## Rodando

```bash
# interface web do ADK
uv run adk web operador_conta

# ou via terminal
uv run adk run operador_conta
```

Acesse `http://localhost:8000` e informe o `cliente_id` para iniciar o atendimento.

## Estrutura

```
operador_conta/
└── agent.py   # definição do agente e ferramentas
main.py        # script de entrada (PyCharm template)
```