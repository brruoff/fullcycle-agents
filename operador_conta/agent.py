from google.adk import Agent
# from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.tool_context import ToolContext


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

ASSINATURAS: dict[str, dict] = {
    "cliente_123": {
        "plano": "Pro",
        "status": "renovacao",
        "data_renuncia": "2026-07-01",
    }
}

def cancelar_assinatura(cliente_id: str, senha: str, tool_context: ToolContext) -> dict:
    """
    Cancela a assinatura do cliente com base no ID do cliente.
    :param
        cliente_id (str): O ID do cliente para a qual a assinatura deve ser cancelada
        senha (str): Senha de confirmação
    :return:
        dict: Dicionário contendo o status da assinatura ou mensagem de erro
    """

    if tool_context.tool_confirmation is None:
        tool_context.request_confirmation(
            hint="Você deseja cancelar a assinatura?",
            payload={'cliente_id': cliente_id, "senha": ""}
        )
        return { "status": "aguardando_confirmacao" }

    if tool_context.tool_confirmation.confirmed is False:
        return { "status": "nao_cancelado", "message": "Assinatura não cancelada" }

    if senha != "1234":
        return { "status": "nao_cancelado", "message": "Senha inválida" }

    assinatura = ASSINATURAS.get(cliente_id)
    if assinatura is not None:
        ASSINATURAS[cliente_id]["status"] = "cancelada"
        return { "status": "cancelado", "message": "Assinatura cancelada" }
    else:
        return { "status": "nao_cancelado", "message": "Cliente não encontrado" }

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
    tools=[
        listar_faturas,
        # FunctionTool(cancelar_assinatura, require_confirmation=True)
        cancelar_assinatura
    ]
)


# agente smell

# docker -> docker models -> llamacpp -> qwen, deepseek

# n8n (agents) -> automação de processos -> processos deterministicos