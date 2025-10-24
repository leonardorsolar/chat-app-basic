# Chat App Basic

Aplicação de chat básica com frontend em React e dois backends disponíveis (Node.js e Python).

## 📁 Estrutura do Projeto

```
chat-app-basic/
│
├── frontend/                    # Aplicação React + TypeScript + Vite
│   ├── src/
│   │   ├── App.tsx             # Componente principal
│   │   ├── main.tsx            # Ponto de entrada
│   │   ├── index.css           # Estilos globais
│   │   ├── components/
│   │   │   ├── Chat.tsx        # Componente do chat
│   │   │   └── ui/             # Componentes UI (Shadcn)
│   │   │       ├── button.tsx
│   │   │       ├── card.tsx
│   │   │       ├── input.tsx
│   │   │       └── scroll-area.tsx
│   │   └── lib/
│   │       └── utils.ts        # Utilitários
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── tsconfig.json
│
├── backend_node/                # Backend Node.js + Express
│   ├── server.ts               # Servidor Express
│   ├── package.json
│   ├── tsconfig.json
│   ├── README.md
│   └── VALIDACAO_MENSAGENS.md
│
├── backend_python/              # Backend Python + FastAPI
│   ├── main.py                 # Servidor FastAPI
│   ├── schemas.py              # Schemas Pydantic
│   ├── test_validation.py      # Testes
│   ├── validation_examples.py  # Exemplos de validação
│   ├── pyproject.toml
│   ├── README.md
│   ├── VALIDATION_GUIDE.md
│   └── LOGGING_GUIDE.md
│
└── README.md                    # Este arquivo
```

## 🚀 Tecnologias

### Frontend

-   **React 18** - Biblioteca UI
-   **TypeScript** - Tipagem estática
-   **Vite** - Build tool
-   **Tailwind CSS** - Estilização
-   **Shadcn/ui** - Componentes UI
-   **Radix UI** - Componentes acessíveis

### Backend Node.js

-   **Express** - Framework web
-   **TypeScript** - Tipagem estática
-   **CORS** - Middleware para CORS
-   **tsx** - Executor TypeScript

### Backend Python

-   **FastAPI** - Framework web moderno
-   **Pydantic** - Validação de dados
-   **Uvicorn** - Servidor ASGI
-   **Poetry** - Gerenciador de dependências

## 📦 Instalação e Execução

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Acesse: `http://localhost:5173`

**Nota:** Configure a URL do backend no arquivo `src/components/Chat.tsx`:

-   Node.js: `http://localhost:3001/api/chat`
-   Python: `http://localhost:3002/api/chat`

### Backend Node.js (Porta 3001)

```bash
cd backend_node
npm install
npm run dev
```

### Backend Python (Porta 3002)

```bash
cd backend_python
poetry install
poetry run uvicorn main:app --reload --port 3002
```

## 🔌 API Endpoints

### Node.js Backend

-   `GET /` - Status do servidor
-   `POST /api/chat` - Enviar mensagem
    ```json
    {
        "message": "Olá!"
    }
    ```

### Python Backend

-   `GET /` - Status do servidor
-   `POST /api/chat` - Enviar mensagem (com validação Pydantic)
-   `GET /health` - Health check
-   `GET /docs` - Documentação interativa (Swagger)
-   `GET /redoc` - Documentação alternativa (ReDoc)

## 📚 Como Usar o Swagger (Backend Python)

O FastAPI gera automaticamente uma documentação interativa da API usando Swagger UI.

### Acessando o Swagger

1. **Inicie o backend Python:**

    ```bash
    cd backend_python
    poetry run uvicorn main:app --reload --port 3002
    ```

2. **Acesse a documentação Swagger:**

    Abra no navegador: `http://localhost:3002/docs`

### Funcionalidades do Swagger UI

-   **📖 Visualizar Endpoints** - Lista todos os endpoints disponíveis organizados por tags
-   **🧪 Testar API** - Execute requisições diretamente pela interface
-   **📝 Ver Schemas** - Visualize os modelos de dados (Pydantic schemas)
-   **📋 Exemplos** - Veja exemplos de request/response para cada endpoint

### Como Testar um Endpoint

1. Clique no endpoint que deseja testar (ex: `POST /api/chat`)
2. Clique no botão **"Try it out"**
3. Preencha o corpo da requisição:
    ```json
    {
        "message": "Olá, como você está?"
    }
    ```
4. Clique em **"Execute"**
5. Veja a resposta abaixo com o código de status e o corpo da resposta

### Documentação Alternativa - ReDoc

Para uma visualização mais limpa e focada em documentação:

Acesse: `http://localhost:3002/redoc`

### Benefícios

-   ✅ Teste a API sem precisar de ferramentas externas (Postman, Insomnia)
-   ✅ Documentação sempre atualizada automaticamente
-   ✅ Validação em tempo real dos dados de entrada
-   ✅ Visualização clara dos tipos de dados esperados e retornados

## 💡 Funcionalidades

-   ✅ Interface de chat responsiva e moderna
-   ✅ Mensagens em tempo real
-   ✅ Respostas automáticas do bot
-   ✅ Validação de mensagens
-   ✅ Tratamento de erros
-   ✅ Logging estruturado (Python)
-   ✅ Documentação automática (Python - FastAPI)

## 🎨 UI Components

O projeto usa componentes customizados do Shadcn/ui:

-   `Button` - Botões estilizados
-   `Card` - Containers de conteúdo
-   `Input` - Campos de entrada
-   `ScrollArea` - Área de rolagem customizada

## 📝 Notas

-   O frontend pode se conectar a qualquer um dos backends
-   Ambos os backends implementam a mesma API REST
-   O backend Python inclui validação avançada com Pydantic
-   O backend Node.js é mais simples e direto
