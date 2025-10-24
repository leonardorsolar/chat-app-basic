# 🎯 Melhores Formas de Validar Entrada e Saída em @app.post()

## 📊 Comparação Rápida

| Método                         | Dificuldade | Segurança  | Recomendado | Uso                |
| ------------------------------ | ----------- | ---------- | ----------- | ------------------ |
| **Pydantic + field_validator** | ⭐⭐        | 🛡️🛡️🛡️🛡️🛡️ | ✅ SIM      | Produção           |
| **Pydantic básico**            | ⭐          | 🛡️🛡️🛡️🛡️   | ✅ SIM      | Projetos pequenos  |
| **Annotated + Field**          | ⭐          | 🛡️🛡️🛡️🛡️   | ✅ SIM      | Validações simples |
| **Validação Manual**           | ⭐⭐⭐      | 🛡️🛡️🛡️     | ⚠️ Às vezes | Casos especiais    |
| **Sem validação**              | -           | -          | ❌ NUNCA    | -                  |

---

## 🏆 OPÇÃO 1: Pydantic com field_validator (MELHOR PRÁTICA)

### ✅ Por que usar?

-   ✅ Validação automática
-   ✅ Mensagens de erro claras
-   ✅ Documentação automática no Swagger
-   ✅ Reutilizável em todo o projeto
-   ✅ Type-safe com mypy
-   ✅ Sanitização automática

### 📝 Exemplo Completo

```python
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class ChatRequest(BaseModel):
    """Schema de entrada com validações robustas"""

    message: str = Field(
        ...,                    # Campo obrigatório
        min_length=1,           # Mínimo 1 caractere
        max_length=1000,        # Máximo 1000 caracteres
        description="Mensagem do usuário"
    )

    user_id: Optional[str] = Field(
        None,
        pattern=r'^[a-zA-Z0-9_-]+$',  # Regex para formato
        description="ID do usuário (opcional)"
    )

    @field_validator('message')
    @classmethod
    def validate_message(cls, v: str) -> str:
        """Validação customizada"""
        # Remove espaços extras
        v = v.strip()

        # Verifica se está vazia
        if not v:
            raise ValueError('Mensagem não pode estar vazia')

        # Verifica conteúdo alfanumérico
        if not any(c.isalnum() for c in v):
            raise ValueError('Mensagem deve ter ao menos um caractere alfanumérico')

        # Remove espaços múltiplos
        v = ' '.join(v.split())

        return v


class ChatResponse(BaseModel):
    """Schema de saída com metadata"""

    reply: str = Field(..., description="Resposta do bot")
    timestamp: str = Field(..., description="ISO timestamp")
    message_length: int = Field(..., description="Tamanho da mensagem")
    processing_time: float = Field(..., description="Tempo em segundos")


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Endpoint com validação automática

    Pydantic automaticamente:
    - Valida tipos
    - Verifica campos obrigatórios
    - Aplica validadores customizados
    - Retorna 422 com detalhes de erro
    """
    # A mensagem aqui já está validada e limpa!
    logger.info(f"Mensagem validada: {request.message}")

    return ChatResponse(
        reply="Resposta...",
        timestamp=datetime.utcnow().isoformat(),
        message_length=len(request.message),
        processing_time=0.5
    )
```

---

## 🎯 OPÇÃO 2: Pydantic Básico (Para Projetos Simples)

### 📝 Exemplo

```python
class SimpleRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)

@app.post("/chat")
async def chat(request: SimpleRequest):
    return {"reply": f"Você disse: {request.message}"}
```

**Quando usar:**

-   ✅ Projetos pequenos
-   ✅ Validações básicas suficientes
-   ✅ Prototipagem rápida

---

## 🔧 OPÇÃO 3: Annotated + Field (Python 3.9+)

### 📝 Exemplo

```python
from typing import Annotated

MessageStr = Annotated[
    str,
    Field(min_length=1, max_length=1000, description="Mensagem")
]

@app.post("/chat")
async def chat(message: MessageStr = Body(...)):
    return {"reply": message}
```

**Quando usar:**

-   ✅ Validações inline
-   ✅ Código mais limpo
-   ✅ Validações simples

---

## ⚠️ OPÇÃO 4: Validação Manual (Casos Especiais)

### 📝 Exemplo

```python
@app.post("/chat")
async def chat(message: str = Body(...)):
    # Validação manual
    message = message.strip()

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Mensagem vazia"
        )

    if len(message) > 1000:
        raise HTTPException(
            status_code=400,
            detail="Mensagem muito longa"
        )

    return {"reply": message}
```

**Quando usar:**

-   ⚠️ Apenas quando Pydantic não for suficiente
-   ⚠️ Lógica de negócio muito complexa
-   ⚠️ Integração com sistemas legados

**Desvantagens:**

-   ❌ Mais código
-   ❌ Sem documentação automática
-   ❌ Mensagens de erro inconsistentes
-   ❌ Difícil de manter

---

## 📊 Como Verificar Entrada e Saída?

### 1️⃣ Logging Estruturado

```python
import logging

logger = logging.getLogger(__name__)

@app.post("/chat")
async def chat(request: ChatRequest):
    # Log de entrada
    logger.info(
        f"📥 ENTRADA | User: {request.user_id} | "
        f"Message: '{request.message}' | "
        f"Length: {len(request.message)}"
    )

    # Processar...
    response = process_message(request.message)

    # Log de saída
    logger.info(
        f"📤 SAÍDA | Reply: '{response[:50]}...' | "
        f"Time: {processing_time}s"
    )

    return response
```

### 2️⃣ Middleware de Logging

```python
import time
from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    # Log entrada
    logger.info(f"📥 {request.method} {request.url}")

    # Processar request
    response = await call_next(request)

    # Log saída
    duration = time.time() - start_time
    logger.info(
        f"📤 {request.method} {request.url} | "
        f"Status: {response.status_code} | "
        f"Time: {duration:.3f}s"
    )

    return response
```

### 3️⃣ Testes Automatizados

```python
def test_mensagem_valida():
    response = client.post(
        "/api/chat",
        json={"message": "Olá"}
    )
    assert response.status_code == 200
    assert "reply" in response.json()

def test_mensagem_vazia():
    response = client.post(
        "/api/chat",
        json={"message": ""}
    )
    assert response.status_code == 422  # Validation error
```

---

## 🔒 Checklist de Segurança

### Validações Essenciais:

-   ✅ **Tamanho mínimo/máximo** - Previne DoS
-   ✅ **Tipo de dados** - Previne erros
-   ✅ **Caracteres permitidos** - Previne XSS/injection
-   ✅ **Sanitização** - Remove dados perigosos
-   ✅ **Rate limiting** - Previne abuso
-   ✅ **Logging** - Auditoria
-   ✅ **Validação de negócio** - Regras da aplicação

### Exemplo Completo de Segurança:

```python
class SecureMessage(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Mensagem (1-1000 chars)"
    )

    @field_validator('message')
    @classmethod
    def sanitize_message(cls, v: str) -> str:
        import html

        # Remove espaços extras
        v = v.strip()

        # Escape HTML (XSS prevention)
        v = html.escape(v)

        # Verifica conteúdo
        if not v:
            raise ValueError('Mensagem vazia')

        # Remove caracteres de controle
        v = ''.join(char for char in v if ord(char) >= 32 or char in '\n\r\t')

        return v
```

---

## 📈 Monitoramento de Entrada/Saída

### Métricas Importantes:

```python
from prometheus_client import Counter, Histogram

# Contadores
messages_total = Counter('messages_total', 'Total de mensagens')
messages_errors = Counter('messages_errors', 'Erros de validação')

# Histograma de tempo
message_duration = Histogram('message_duration_seconds', 'Tempo de processamento')

@app.post("/chat")
async def chat(request: ChatRequest):
    messages_total.inc()  # Incrementa contador

    with message_duration.time():  # Mede tempo
        try:
            response = process_message(request.message)
            return response
        except Exception as e:
            messages_errors.inc()  # Incrementa erros
            raise
```

---

## 🎓 Resumo Final

### ✅ FAÇA:

1. **Use Pydantic** para validação
2. **Adicione field_validator** para lógica customizada
3. **Configure logging** estruturado
4. **Escreva testes** automatizados
5. **Documente** suas validações
6. **Sanitize** dados de entrada
7. **Monitore** métricas

### ❌ NÃO FAÇA:

1. ❌ Confiar em dados do usuário sem validação
2. ❌ Usar validação manual quando Pydantic serve
3. ❌ Ignorar mensagens de erro
4. ❌ Esquecer de fazer logging
5. ❌ Pular testes de validação
6. ❌ Usar print() ao invés de logger
7. ❌ Expor detalhes internos em mensagens de erro

---

## 🚀 Comandos Úteis

```bash
# Instalar dependências
poetry install

# Rodar servidor
poetry run python main.py

# Rodar testes
poetry run pytest test_validation.py -v

# Rodar com coverage
poetry run pytest --cov=main --cov-report=html

# Ver exemplos
poetry run python validation_examples.py

# Documentação interativa
# http://localhost:3002/docs
```

---

## 📚 Recursos Adicionais

-   [FastAPI Docs - Request Body](https://fastapi.tiangolo.com/tutorial/body/)
-   [Pydantic Docs - Validators](https://docs.pydantic.dev/latest/concepts/validators/)
-   [FastAPI Docs - Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/)
