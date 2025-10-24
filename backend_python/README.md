# Chatbot Backend - Python FastAPI

Backend do chatbot desenvolvido com FastAPI, Pydantic e Poetry.

## 🚀 Tecnologias

-   **FastAPI**: Framework web moderno e rápido para construir APIs
-   **Pydantic**: Validação de dados e tipagem forte
-   **Poetry**: Gerenciador de dependências e empacotamento
-   **Uvicorn**: Servidor ASGI de alta performance

## 📋 Pré-requisitos

-   Python 3.9 ou superior
-   Poetry (instalado globalmente)

### Instalar Poetry

```bash
# Linux, macOS, Windows (WSL)
curl -sSL https://install.python-poetry.org | python3 -

# Ou via pip
pip install poetry
```

## 🔧 Instalação

1. Clone o repositório e navegue até a pasta do backend:

```bash
cd backend_python
```

2. Instale as dependências com Poetry:

```bash
poetry install
```

Isso criará automaticamente um ambiente virtual e instalará todas as dependências necessárias.

## ▶️ Executando o Projeto

### Opção 1: Usando Poetry (Recomendado)

```bash
poetry run python main.py
```

### Opção 2: Ativando o ambiente virtual

```bash
# Ativar o ambiente virtual
poetry shell

# Executar o servidor
python main.py
```

### Opção 3: Usando Uvicorn diretamente

```bash
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 3001
```

O servidor estará disponível em:

-   **API**: http://localhost:3001
-   **Documentação Interativa (Swagger)**: http://localhost:3001/docs
-   **Documentação Alternativa (ReDoc)**: http://localhost:3001/redoc

## 📡 Endpoints

### GET `/`

Rota raiz que retorna uma mensagem de boas-vindas.

**Resposta:**

```json
{
    "message": "Servidor do Chatbot está rodando!"
}
```

### POST `/api/chat`

Endpoint principal do chat. Recebe uma mensagem e retorna uma resposta do bot.

**Request Body:**

```json
{
    "message": "Olá, como você está?"
}
```

**Response:**

```json
{
    "reply": "Olá! Como posso ajudar você hoje? 😊",
    "timestamp": "2025-10-24T10:30:00.000Z"
}
```

### GET `/health`

Rota de health check para verificar o status do servidor.

**Resposta:**

```json
{
    "status": "ok",
    "message": "Servidor está funcionando!"
}
```

## 📝 Estrutura do Projeto

```
backend_python/
├── main.py           # Arquivo principal com as rotas FastAPI
├── schemas.py        # Modelos Pydantic para validação
├── pyproject.toml    # Configuração do Poetry e dependências
└── README.md         # Documentação
```

## 🧪 Testando a API

### Usando curl:

```bash
# Testar rota raiz
curl http://localhost:3001/

# Testar chat
curl -X POST http://localhost:3001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Olá!"}'

# Testar health check
curl http://localhost:3001/health
```

### Usando a documentação interativa:

Acesse http://localhost:3001/docs e teste os endpoints diretamente no navegador!

## 🔄 Comparação com a versão Express/TypeScript

Esta implementação mantém a mesma lógica do servidor Express original, com as seguintes melhorias:

-   ✅ Tipagem forte com Pydantic
-   ✅ Validação automática de dados
-   ✅ Documentação automática da API (Swagger/OpenAPI)
-   ✅ Suporte assíncrono nativo
-   ✅ Melhor performance com Uvicorn
-   ✅ Gerenciamento de dependências com Poetry

## 📦 Comandos Úteis do Poetry

```bash
# Adicionar nova dependência
poetry add nome-do-pacote

# Adicionar dependência de desenvolvimento
poetry add --group dev nome-do-pacote

# Atualizar dependências
poetry update

# Ver dependências instaladas
poetry show

# Exportar requirements.txt
poetry export -f requirements.txt --output requirements.txt
```

## 🐛 Debug

Para ativar o modo debug e ver logs detalhados:

```bash
poetry run uvicorn main:app --reload --log-level debug --port 3001
```

## 📄 Licença

Este projeto é open source e está disponível sob a licença MIT.
