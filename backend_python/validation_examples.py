"""
Exemplos de diferentes abordagens para validação de entrada/saída no FastAPI

Este arquivo demonstra as melhores práticas para verificar mensagens em endpoints.
"""

from fastapi import FastAPI, HTTPException, status, Body, Query
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional, Annotated
from datetime import datetime
import logging

# Configurar logging
logger = logging.getLogger(__name__)

# ============================================================================
# ABORDAGEM 1: Validação com Pydantic (RECOMENDADA)
# ============================================================================
# Vantagens:
# - Validação automática
# - Mensagens de erro claras
# - Documentação automática no Swagger
# - Reutilizável em múltiplos endpoints

class MessageValidated(BaseModel):
    """Modelo com validações robustas usando Pydantic"""
    
    message: str = Field(
        ...,  # Campo obrigatório
        min_length=1,
        max_length=1000,
        description="Mensagem do usuário (1-1000 caracteres)",
        examples=["Olá, como você está?"]
    )
    
    user_id: Optional[str] = Field(
        None,
        pattern=r'^[a-zA-Z0-9_-]+$',  # Regex para validar formato
        min_length=3,
        max_length=50,
        description="ID do usuário (opcional)"
    )
    
    @field_validator('message')
    @classmethod
    def validate_message_content(cls, v: str) -> str:
        """Validação customizada da mensagem"""
        v = v.strip()
        
        if not v:
            raise ValueError('Mensagem não pode estar vazia')
        
        if not any(c.isalnum() for c in v):
            raise ValueError('Mensagem deve conter pelo menos um caractere alfanumérico')
        
        # Remove espaços múltiplos
        v = ' '.join(v.split())
        
        return v


# ============================================================================
# ABORDAGEM 2: Validação Manual no Endpoint
# ============================================================================
# Vantagens:
# - Controle total sobre a lógica
# - Útil para validações complexas específicas do negócio

def validate_message_manual(message: str) -> tuple[bool, str]:
    """
    Valida mensagem manualmente
    
    Returns:
        (is_valid, error_message)
    """
    if not message:
        return False, "Mensagem não pode estar vazia"
    
    message = message.strip()
    
    if len(message) < 1:
        return False, "Mensagem muito curta"
    
    if len(message) > 1000:
        return False, "Mensagem muito longa (máximo 1000 caracteres)"
    
    if not any(c.isalnum() for c in message):
        return False, "Mensagem deve conter pelo menos um caractere alfanumérico"
    
    # Verificar palavras proibidas (exemplo)
    forbidden_words = ['spam', 'hack']
    if any(word in message.lower() for word in forbidden_words):
        return False, "Mensagem contém conteúdo proibido"
    
    return True, ""


# ============================================================================
# ABORDAGEM 3: Validação com Annotated (Python 3.9+)
# ============================================================================
# Vantagens:
# - Sintaxe mais limpa
# - Validação inline
# - Boa para validações simples

MessageStr = Annotated[
    str,
    Field(
        min_length=1,
        max_length=1000,
        description="Mensagem do usuário"
    )
]


# ============================================================================
# ABORDAGEM 4: Validação com Query Parameters
# ============================================================================
# Útil para endpoints GET com parâmetros de query

QueryMessage = Annotated[
    str,
    Query(
        min_length=1,
        max_length=500,
        description="Mensagem como parâmetro de query",
        examples=["Olá"]
    )
]


# ============================================================================
# EXEMPLOS DE USO NOS ENDPOINTS
# ============================================================================

app = FastAPI(title="Exemplos de Validação")


# EXEMPLO 1: Usando Pydantic Model (MELHOR PRÁTICA)
@app.post("/chat/v1")
async def chat_with_pydantic(request: MessageValidated):
    """
    ✅ RECOMENDADO: Validação automática com Pydantic
    
    - Pydantic valida automaticamente
    - Erros retornam 422 com detalhes
    - Documentação automática no Swagger
    """
    logger.info(f"Mensagem: {request.message}, User: {request.user_id}")
    
    return {
        "reply": f"Recebi sua mensagem: {request.message}",
        "validated": True
    }


# EXEMPLO 2: Validação Manual
@app.post("/chat/v2")
async def chat_with_manual_validation(message: str = Body(...)):
    """
    ⚠️ Validação manual - Mais trabalho, mas controle total
    """
    is_valid, error_msg = validate_message_manual(message)
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )
    
    return {"reply": f"Mensagem validada: {message}"}


# EXEMPLO 3: Usando Annotated
@app.post("/chat/v3")
async def chat_with_annotated(message: MessageStr = Body(...)):
    """
    ✅ Boa opção: Validação inline com Annotated
    """
    return {"reply": f"Mensagem: {message}"}


# EXEMPLO 4: Query Parameters
@app.get("/chat/v4")
async def chat_with_query(message: QueryMessage):
    """
    ✅ Para endpoints GET
    """
    return {"reply": f"Query: {message}"}


# EXEMPLO 5: Validação com Try/Except (para casos especiais)
@app.post("/chat/v5")
async def chat_with_try_except(data: dict):
    """
    ⚠️ Validação com try/except - útil para dados complexos
    """
    try:
        # Tenta validar com Pydantic
        validated = MessageValidated(**data)
        
        return {
            "reply": f"Mensagem: {validated.message}",
            "user": validated.user_id
        }
        
    except ValidationError as e:
        logger.error(f"Erro de validação: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors()
        )


# ============================================================================
# EXEMPLO 6: Logging completo de entrada/saída
# ============================================================================

class ChatRequestLogged(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    
    @field_validator('message')
    @classmethod
    def log_and_validate(cls, v: str) -> str:
        logger.info(f"📥 ENTRADA: '{v}' (tamanho: {len(v)})")
        v = v.strip()
        if not v:
            raise ValueError('Mensagem vazia')
        return v


class ChatResponseLogged(BaseModel):
    reply: str
    timestamp: str
    
    def model_post_init(self, __context) -> None:
        """Hook executado após criação do modelo"""
        logger.info(f"📤 SAÍDA: '{self.reply}' em {self.timestamp}")


@app.post("/chat/logged", response_model=ChatResponseLogged)
async def chat_with_logging(request: ChatRequestLogged):
    """
    ✅ MELHOR PRÁTICA: Logging automático de entrada e saída
    """
    response = ChatResponseLogged(
        reply=f"Resposta para: {request.message}",
        timestamp=datetime.utcnow().isoformat()
    )
    
    return response


# ============================================================================
# COMPARAÇÃO E RECOMENDAÇÕES
# ============================================================================

"""
🏆 RANKING DE MELHORES PRÁTICAS:

1. ✅ Pydantic Model com field_validator (RECOMENDADO)
   - Validação automática
   - Reutilizável
   - Documentação automática
   - Mensagens de erro claras

2. ✅ Annotated com Field
   - Sintaxe limpa
   - Boa para validações simples
   - Menos reutilizável

3. ⚠️ Validação Manual
   - Use apenas quando Pydantic não for suficiente
   - Mais código para manter
   - Erros podem não ser consistentes

4. ❌ Sem validação
   - NUNCA faça isso em produção!


📝 DICAS:

1. Use Pydantic para validação de dados
2. Adicione logging para debug
3. Retorne erros claros e informativos
4. Documente suas validações
5. Use type hints sempre
6. Teste casos extremos (strings vazias, muito longas, etc)
7. Sanitize inputs (strip, lower, etc)
8. Considere validações de segurança (XSS, SQL injection)


🔒 SEGURANÇA:

- Sempre valide tamanho máximo (DoS)
- Sanitize HTML/JavaScript (XSS)
- Valide caracteres especiais
- Log tentativas suspeitas
- Rate limiting em produção
"""

if __name__ == "__main__":
    import uvicorn
    print("📚 Servidor de exemplos de validação")
    print("📖 Acesse http://localhost:8000/docs para ver a documentação")
    uvicorn.run(app, host="0.0.0.0", port=8000)
