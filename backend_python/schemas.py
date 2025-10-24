from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


class ChatRequest(BaseModel):
    """Schema para requisição de mensagem do chat"""
    message: str = Field(
        ..., 
        min_length=1,
        max_length=1000,
        description="Mensagem do usuário"
    )
    user_id: Optional[str] = Field(
        None,
        description="ID opcional do usuário"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "Olá, como você está?",
                    "user_id": "user123"
                }
            ]
        }
    }
    
    @field_validator('message')
    @classmethod
    def validate_message(cls, v: str) -> str:
        """
        Validação customizada da mensagem:
        - Remove espaços extras
        - Verifica se não está vazia após strip
        - Valida caracteres permitidos
        """
        # Remove espaços em branco no início e fim
        v = v.strip()
        
        # Verifica se está vazia após strip
        if not v:
            raise ValueError('Mensagem não pode estar vazia ou conter apenas espaços')
        
        # Verifica se tem conteúdo significativo (não apenas pontuação)
        if not any(c.isalnum() for c in v):
            raise ValueError('Mensagem deve conter pelo menos um caractere alfanumérico')
        
        return v


class ChatResponse(BaseModel):
    """Schema para resposta do chat"""
    reply: str = Field(..., description="Resposta do bot")
    timestamp: str = Field(..., description="Timestamp da resposta")
    message_length: Optional[int] = Field(
        None,
        description="Tamanho da mensagem recebida"
    )
    processing_time: Optional[float] = Field(
        None,
        description="Tempo de processamento em segundos"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "reply": "Olá! Como posso ajudar você hoje? 😊",
                    "timestamp": "2025-10-24T10:30:00.000Z",
                    "message_length": 20,
                    "processing_time": 0.75
                }
            ]
        }
    }


class HealthResponse(BaseModel):
    """Schema para resposta de health check"""
    status: str
    message: str


class ErrorResponse(BaseModel):
    """Schema para resposta de erro"""
    error: str
