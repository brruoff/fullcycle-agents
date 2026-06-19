from uuid import UUID

from fastapi import FastAPI
from pydantic import BaseModel
from operador_conta.agent import root_agent as operador_conta_agent
from google.adk.apps import App
from google.adk import Runner, sessions
from google.adk.sessions import InMemorySessionService
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Operador Conta API",
    description="API para gerenciar assinaturas e faturas",
    version="1.0.0"
)

class MensagemRequest(BaseModel):
    mensagem: str
    sessao_id: str | None = None

adk_app = App(
    name=operador_conta_agent.name,
    root_agent=operador_conta_agent,
    # context_cache_config= cache/compactação
    # plugins= debug/observabilidade
)

session_service = InMemorySessionService()

runner = Runner(app=adk_app, session_service=session_service)

@app.post('/mensagem')
async def mensagem(request: MensagemRequest):
    sessao = await session_service.create_session(
            app_name=adk_app.name,
            user_id="user-1"
        ) if not request.sessao_id else \
            await session_service.get_session(
                app_name=adk_app.name,
                user_id="user-1",
                session_id=request.sessao_id,
            )
    if not sessao:
        raise ValueError("Sessão não encontrada")

    conteudo = types.Content(
        role="user",
        parts=[types.Part.from_text(text=request.mensagem)]
    )

    async for event in runner.run_async(
        user_id="user-1",
        session_id=sessao.id,
        new_message=conteudo
    ):
        if event.is_final_response() and event.content and event.content.parts:
            return { "resposta": event.content.parts[0].text, "sessao_id": sessao.id }
