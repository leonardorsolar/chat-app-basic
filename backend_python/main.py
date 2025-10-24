from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import asyncio
import random
import logging
import time
from typing import Dict

from schemas import ChatRequest, ChatResponse, HealthResponse, ErrorResponse

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Chatbot Backend API",
    description="Backend do Chatbot usando FastAPI e Pydantic",
    version="1.0.0"
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Respostas automáticas do bot
BOT_RESPONSES = [
    "Interessante! Me conte mais sobre isso.",
    "Entendo o que você está dizendo.",
    "Isso é muito legal! Continue...",
    "Hmm, deixe-me pensar sobre isso...",
    "Ótima pergunta! Aqui está o que penso:",
    "Posso ajudar você com isso!",
    "Isso me lembra de algo importante.",
    "Vamos explorar essa ideia juntos!",
]


@app.get("/", tags=["Root"])
async def root() -> Dict[str, str]:
    """Rota raiz do servidor"""
    return {"message": "Servidor do Chatbot está rodando!"}


@app.post(
    "/api/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Mensagem inválida"},
        422: {"description": "Erro de validação dos dados"}
    },
    tags=["Chat"],
    summary="Enviar mensagem ao chatbot",
    description="Recebe uma mensagem do usuário e retorna uma resposta do bot com metadata"
)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Endpoint principal do chat.
    
    Validações realizadas:
    - Mensagem não pode estar vazia
    - Mensagem deve ter entre 1 e 1000 caracteres
    - Mensagem deve conter pelo menos um caractere alfanumérico
    
    Retorna:
    - reply: Resposta do bot
    - timestamp: Horário da resposta
    - message_length: Tamanho da mensagem original
    - processing_time: Tempo de processamento
    """
    start_time = time.time()
    
    # Log da mensagem recebida (já validada pelo Pydantic)
    logger.info(f"📨 Mensagem recebida: '{request.message}' | User ID: {request.user_id}")
    
    # A mensagem já foi validada e limpa pelo validator do Pydantic
    message = request.message
    message_lower = message.lower()
    
    # Simula um pequeno delay para parecer mais real
    delay = 0.5 + random.random()  # Entre 0.5s e 1.5s
    await asyncio.sleep(delay)
    
    # Seleciona uma resposta aleatória
    reply = random.choice(BOT_RESPONSES)
    
    # Adiciona contexto baseado na mensagem do usuário
    if "olá" in message_lower or "oi" in message_lower:
        reply = "Olá! Como posso ajudar você hoje? 😊"
    elif "como vai" in message_lower:
        reply = "Estou muito bem, obrigado por perguntar! E você, como está?"
    elif "tchau" in message_lower or "adeus" in message_lower:
        reply = "Até logo! Foi um prazer conversar com você! 👋"
    elif "ajuda" in message_lower:
        reply = "Claro! Estou aqui para ajudar. O que você precisa?"
    elif "?" in message:
        reply = f'Boa pergunta! Sobre "{message}", eu diria que é um tópico interessante para explorarmos.'
    
    # Calcula tempo de processamento
    processing_time = time.time() - start_time
    
    # Log da resposta enviada
    logger.info(f"📤 Resposta enviada: '{reply[:50]}...' | Tempo: {processing_time:.3f}s")
    
    return ChatResponse(
        reply=reply,
        timestamp=datetime.utcnow().isoformat() + "Z",
        message_length=len(message),
        processing_time=round(processing_time, 3)
    )


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"]
)
async def health_check() -> HealthResponse:
    """Rota de health check para verificar o status do servidor"""
    return HealthResponse(
        status="ok",
        message="Servidor está funcionando!"
    )


if __name__ == "__main__":
    import uvicorn
    
    PORT = 3002
    
    print(f"🚀 Servidor rodando em http://localhost:{PORT}")
    print(f"📡 API disponível em http://localhost:{PORT}/api/chat")
    print(f"📚 Documentação em http://localhost:{PORT}/docs")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        reload=True
    )

# 1. Instalar dependências
#cd backend_python
#poetry install

# 2. Rodar o servidor
#poetry run python main.py

# 1. Ativar modo debug
# Editar main.py: level=logging.DEBUG

# 2. Rodar aplicação
#poetry run python main.py

# 3. Analisar logs
#poetry run python analyze_logs.py debug.log