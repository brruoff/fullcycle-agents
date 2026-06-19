from google.adk import Agent

FATURAS = [
    {  # dicionario
        "id": "fatura_001",
        "cliente_id": "cliente_123",
        "valor": 49.99,
        "data_emissao": "2024-01-01",
        "data_vencimento": "2024-01-15",
        "status": "paga",
    },
    {
        "id": "fatura_002",
        "cliente_id": "cliente_123",
        "valor": 49.99,
        "data_emissao": "2024-02-01",
        "data_vencimento": "2024-02-15",
        "status": "pendente",
    },
]

def listar_faturas(client_id: str) -> dict:
    # db, http, integracao
    """
    Busca as faturas do cliente com base no ID do cliente.
    :param
        client_id (str): ID do cliente para o qual as faturas devem ser buscadas
    :return:
        dict: Dicionário contendo as faturas do cliente ou mensagem de erro
    """
    faturas_cliente = [fatura for fatura in FATURAS if fatura["cliente_id"] == client_id]
    return { 'faturas': faturas_cliente }

root_agent = Agent(
    name='root_agent',
    model='gemini-3.1-flash-lite',
    #model=litellm('llamacpp') usado para modelos locais (docker models -> llm)
    instruction="""
        Você é um atendente de conta interativo da Full Cycle.
        Você é responsável por:
        - Informar ao cliente sobre sua assinatura: o plano, status e renovação.
        - Tirar dúvidas sobre as faturas do cliente.
        - Cancelar a assinatura do cliente, se solicitado.
        O usuário precisa fornecer o ID do cliente para que você possa buscar as informações corretas.
        Seja cordial e direto.
    """,
    tools=[listar_faturas]
)


# agente smell

# docker -> docker models -> llamacpp -> qwen, deepseek

# n8n (agents) -> automação de processos -> processos deterministicos