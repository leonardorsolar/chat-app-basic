# Guia de Validação de Mensagens - Backend Chat

## 📋 Índice

1. [Código Atual](#código-atual)
2. [Problemas Identificados](#problemas-identificados)
3. [Soluções Propostas](#soluções-propostas)
4. [Implementação com Zod](#implementação-com-zod)
5. [Implementação com Validação Manual](#implementação-com-validação-manual)
6. [Middleware Reutilizável](#middleware-reutilizável)
7. [Comparação de Abordagens](#comparação-de-abordagens)

---

## 📝 Código Atual

```typescript
app.post("/api/chat", (req: Request, res: Response) => {
    const { message } = req.body

    if (!message) {
        return res.status(400).json({ error: "Mensagem é obrigatória" })
    }

    console.log(`Mensagem recebida: ${message}`)

    // Resto do código...
})
```

### ⚠️ Problemas Identificados

1. **Validação Incompleta**: Apenas verifica se `message` existe
2. **Sem Validação de Tipo**: Não verifica se é string
3. **Sem Limite de Tamanho**: Permite mensagens muito longas
4. **Sem Sanitização**: Vulnerável a XSS e injeções
5. **Sem Validação de Saída**: Resposta não tem estrutura garantida

---

## 🎯 Soluções Propostas

## Implementação com Zod

### 🔹 Vantagens

-   ✅ Validação declarativa e type-safe
-   ✅ Mensagens de erro automáticas
-   ✅ Inferência de tipos TypeScript
-   ✅ Reutilizável e manutenível

### Instalação

```bash
npm install zod
```

### Código Completo

```typescript
import express, { Request, Response } from "express"
import cors from "cors"
import { z } from "zod"

const app = express()
const PORT = 3001

// Middleware
app.use(cors())
app.use(express.json())

// ===== SCHEMAS DE VALIDAÇÃO =====

// Schema para entrada (request)
const messageInputSchema = z.object({
    message: z
        .string({
            required_error: "Mensagem é obrigatória",
            invalid_type_error: "Mensagem deve ser texto",
        })
        .min(1, "Mensagem não pode estar vazia")
        .max(1000, "Mensagem muito longa (máximo 1000 caracteres)")
        .trim(),
    userId: z.string().optional(),
    metadata: z.record(z.any()).optional(),
})

// Schema para saída (response)
const messageOutputSchema = z.object({
    reply: z.string(),
    timestamp: z.string(),
    messageId: z.string().optional(),
    status: z.enum(["success", "error"]),
})

// Types inferidos automaticamente
type MessageInput = z.infer<typeof messageInputSchema>
type MessageOutput = z.infer<typeof messageOutputSchema>

// ===== RESPOSTAS DO BOT =====

const botResponses = [
    "Interessante! Me conte mais sobre isso.",
    "Entendo o que você está dizendo.",
    "Isso é muito legal! Continue...",
    "Hmm, deixe-me pensar sobre isso...",
    "Ótima pergunta! Aqui está o que penso:",
    "Posso ajudar você com isso!",
    "Isso me lembra de algo importante.",
    "Vamos explorar essa ideia juntos!",
]

// ===== FUNÇÕES AUXILIARES =====

/**
 * Sanitiza mensagem para prevenir XSS
 */
function sanitizeMessage(message: string): string {
    return message
        .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, "")
        .replace(/<iframe\b[^<]*(?:(?!<\/iframe>)<[^<]*)*<\/iframe>/gi, "")
        .replace(/on\w+\s*=\s*["'][^"']*["']/gi, "")
}

/**
 * Gera resposta contextual do bot
 */
function generateBotReply(message: string): string {
    const lowerMessage = message.toLowerCase()

    if (lowerMessage.includes("olá") || lowerMessage.includes("oi")) {
        return "Olá! Como posso ajudar você hoje? 😊"
    } else if (lowerMessage.includes("como vai")) {
        return "Estou muito bem, obrigado por perguntar! E você, como está?"
    } else if (
        lowerMessage.includes("tchau") ||
        lowerMessage.includes("adeus")
    ) {
        return "Até logo! Foi um prazer conversar com você! 👋"
    } else if (lowerMessage.includes("ajuda")) {
        return "Claro! Estou aqui para ajudar. O que você precisa?"
    } else if (message.includes("?")) {
        return `Boa pergunta! Sobre "${message}", eu diria que é um tópico interessante para explorarmos.`
    }

    // Resposta aleatória padrão
    return botResponses[Math.floor(Math.random() * botResponses.length)]
}

// ===== ROTAS =====

app.get("/", (req: Request, res: Response) => {
    res.send("Servidor do Chatbot está rodando!")
})

/**
 * Rota de chat com validação completa
 */
app.post("/api/chat", (req: Request, res: Response) => {
    try {
        // 1. Validar entrada com Zod
        const validatedInput = messageInputSchema.parse(req.body)

        // 2. Sanitizar mensagem
        const sanitizedMessage = sanitizeMessage(validatedInput.message)

        // 3. Log para debug
        console.log(`Mensagem recebida: ${sanitizedMessage}`)
        console.log(`UserId: ${validatedInput.userId || "anônimo"}`)

        // 4. Simular delay realista
        setTimeout(() => {
            // 5. Gerar resposta
            const reply = generateBotReply(sanitizedMessage)

            // 6. Criar resposta estruturada
            const response: MessageOutput = {
                reply,
                timestamp: new Date().toISOString(),
                messageId: `msg_${Date.now()}_${Math.random()
                    .toString(36)
                    .substr(2, 9)}`,
                status: "success",
            }

            // 7. Validar saída (opcional mas recomendado)
            const validatedOutput = messageOutputSchema.parse(response)

            // 8. Enviar resposta
            res.json(validatedOutput)
        }, 500 + Math.random() * 1000)
    } catch (error) {
        // Tratamento de erros de validação
        if (error instanceof z.ZodError) {
            return res.status(400).json({
                status: "error",
                error: "Dados inválidos",
                details: error.errors.map((err) => ({
                    campo: err.path.join("."),
                    mensagem: err.message,
                })),
            })
        }

        // Erro genérico
        console.error("Erro no processamento:", error)
        return res.status(500).json({
            status: "error",
            error: "Erro interno do servidor",
        })
    }
})

// Rota de health check
app.get("/health", (req: Request, res: Response) => {
    res.json({ status: "ok", message: "Servidor está funcionando!" })
})

// Iniciar servidor
app.listen(PORT, () => {
    console.log(`🚀 Servidor rodando em http://localhost:${PORT}`)
    console.log(`📡 API disponível em http://localhost:${PORT}/api/chat`)
})
```

### Exemplos de Requisições e Respostas

#### ✅ Requisição Válida

```bash
curl -X POST http://localhost:3001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Olá, como vai?"}'
```

**Resposta:**

```json
{
    "reply": "Olá! Como posso ajudar você hoje? 😊",
    "timestamp": "2025-10-24T10:30:00.000Z",
    "messageId": "msg_1729765800000_abc123def",
    "status": "success"
}
```

#### ❌ Requisição Inválida (mensagem vazia)

```bash
curl -X POST http://localhost:3001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": ""}'
```

**Resposta:**

```json
{
    "status": "error",
    "error": "Dados inválidos",
    "details": [
        {
            "campo": "message",
            "mensagem": "Mensagem não pode estar vazia"
        }
    ]
}
```

#### ❌ Requisição Inválida (sem mensagem)

```bash
curl -X POST http://localhost:3001/api/chat \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Resposta:**

```json
{
    "status": "error",
    "error": "Dados inválidos",
    "details": [
        {
            "campo": "message",
            "mensagem": "Mensagem é obrigatória"
        }
    ]
}
```

---

## Implementação com Validação Manual

### 🔹 Vantagens

-   ✅ Sem dependências externas
-   ✅ Controle total sobre validações
-   ✅ Mais leve

### Código Completo

```typescript
import express, { Request, Response } from "express"
import cors from "cors"

const app = express()
const PORT = 3001

// Middleware
app.use(cors())
app.use(express.json())

// ===== INTERFACES =====

interface MessageInput {
    message: string
    userId?: string
    metadata?: Record<string, any>
}

interface MessageOutput {
    reply: string
    timestamp: string
    messageId?: string
    status: "success" | "error"
}

interface ValidationError {
    status: "error"
    error: string
    details?: Array<{ campo: string; mensagem: string }>
}

// ===== RESPOSTAS DO BOT =====

const botResponses = [
    "Interessante! Me conte mais sobre isso.",
    "Entendo o que você está dizendo.",
    "Isso é muito legal! Continue...",
    "Hmm, deixe-me pensar sobre isso...",
    "Ótima pergunta! Aqui está o que penso:",
    "Posso ajudar você com isso!",
    "Isso me lembra de algo importante.",
    "Vamos explorar essa ideia juntos!",
]

// ===== FUNÇÕES DE VALIDAÇÃO =====

/**
 * Valida entrada da mensagem
 */
function validateMessageInput(body: any): {
    isValid: boolean
    data?: MessageInput
    errors?: Array<{ campo: string; mensagem: string }>
} {
    const errors: Array<{ campo: string; mensagem: string }> = []

    // Validar campo 'message'
    if (!body.message) {
        errors.push({ campo: "message", mensagem: "Mensagem é obrigatória" })
    } else if (typeof body.message !== "string") {
        errors.push({ campo: "message", mensagem: "Mensagem deve ser texto" })
    } else {
        const trimmedMessage = body.message.trim()

        if (trimmedMessage.length === 0) {
            errors.push({
                campo: "message",
                mensagem: "Mensagem não pode estar vazia",
            })
        } else if (trimmedMessage.length > 1000) {
            errors.push({
                campo: "message",
                mensagem: "Mensagem muito longa (máximo 1000 caracteres)",
            })
        }
    }

    // Validar campo 'userId' (opcional)
    if (body.userId !== undefined && typeof body.userId !== "string") {
        errors.push({ campo: "userId", mensagem: "UserId deve ser texto" })
    }

    // Se houver erros, retornar inválido
    if (errors.length > 0) {
        return { isValid: false, errors }
    }

    // Retornar dados validados
    return {
        isValid: true,
        data: {
            message: body.message.trim(),
            userId: body.userId,
            metadata: body.metadata,
        },
    }
}

/**
 * Sanitiza mensagem para prevenir XSS
 */
function sanitizeMessage(message: string): string {
    return message
        .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, "")
        .replace(/<iframe\b[^<]*(?:(?!<\/iframe>)<[^<]*)*<\/iframe>/gi, "")
        .replace(/on\w+\s*=\s*["'][^"']*["']/gi, "")
}

/**
 * Gera resposta contextual do bot
 */
function generateBotReply(message: string): string {
    const lowerMessage = message.toLowerCase()

    if (lowerMessage.includes("olá") || lowerMessage.includes("oi")) {
        return "Olá! Como posso ajudar você hoje? 😊"
    } else if (lowerMessage.includes("como vai")) {
        return "Estou muito bem, obrigado por perguntar! E você, como está?"
    } else if (
        lowerMessage.includes("tchau") ||
        lowerMessage.includes("adeus")
    ) {
        return "Até logo! Foi um prazer conversar com você! 👋"
    } else if (lowerMessage.includes("ajuda")) {
        return "Claro! Estou aqui para ajudar. O que você precisa?"
    } else if (message.includes("?")) {
        return `Boa pergunta! Sobre "${message}", eu diria que é um tópico interessante para explorarmos.`
    }

    return botResponses[Math.floor(Math.random() * botResponses.length)]
}

/**
 * Gera ID único para mensagem
 */
function generateMessageId(): string {
    return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
}

// ===== ROTAS =====

app.get("/", (req: Request, res: Response) => {
    res.send("Servidor do Chatbot está rodando!")
})

/**
 * Rota de chat com validação manual completa
 */
app.post("/api/chat", (req: Request, res: Response) => {
    // 1. Validar entrada
    const validation = validateMessageInput(req.body)

    if (!validation.isValid) {
        const errorResponse: ValidationError = {
            status: "error",
            error: "Dados inválidos",
            details: validation.errors,
        }
        return res.status(400).json(errorResponse)
    }

    // 2. Extrair dados validados
    const { message, userId } = validation.data!

    // 3. Sanitizar mensagem
    const sanitizedMessage = sanitizeMessage(message)

    // 4. Log para debug
    console.log(`Mensagem recebida: ${sanitizedMessage}`)
    console.log(`UserId: ${userId || "anônimo"}`)

    // 5. Simular delay realista
    setTimeout(() => {
        try {
            // 6. Gerar resposta
            const reply = generateBotReply(sanitizedMessage)

            // 7. Criar resposta estruturada
            const response: MessageOutput = {
                reply,
                timestamp: new Date().toISOString(),
                messageId: generateMessageId(),
                status: "success",
            }

            // 8. Enviar resposta
            res.json(response)
        } catch (error) {
            console.error("Erro ao processar mensagem:", error)
            res.status(500).json({
                status: "error",
                error: "Erro interno do servidor",
            })
        }
    }, 500 + Math.random() * 1000)
})

// Rota de health check
app.get("/health", (req: Request, res: Response) => {
    res.json({ status: "ok", message: "Servidor está funcionando!" })
})

// Iniciar servidor
app.listen(PORT, () => {
    console.log(`🚀 Servidor rodando em http://localhost:${PORT}`)
    console.log(`📡 API disponível em http://localhost:${PORT}/api/chat`)
})
```

---

## Middleware Reutilizável

### 🔹 Abordagem Modular

Criar middlewares reutilizáveis para separar responsabilidades:

```typescript
// ===== MIDDLEWARES =====

/**
 * Middleware de validação de mensagem
 */
const validateMessage = (req: Request, res: Response, next: Function) => {
    const validation = validateMessageInput(req.body)

    if (!validation.isValid) {
        return res.status(400).json({
            status: "error",
            error: "Dados inválidos",
            details: validation.errors,
        })
    }

    // Adicionar dados validados ao request
    req.body.validated = validation.data
    next()
}

/**
 * Middleware de sanitização
 */
const sanitizeInput = (req: Request, res: Response, next: Function) => {
    if (req.body.validated?.message) {
        req.body.validated.message = sanitizeMessage(req.body.validated.message)
    }
    next()
}

/**
 * Middleware de logging
 */
const logMessage = (req: Request, res: Response, next: Function) => {
    const { message, userId } = req.body.validated || {}
    console.log(
        `[${new Date().toISOString()}] Mensagem de ${
            userId || "anônimo"
        }: ${message}`
    )
    next()
}

// ===== USO DOS MIDDLEWARES =====

app.post(
    "/api/chat",
    validateMessage, // 1. Validar
    sanitizeInput, // 2. Sanitizar
    logMessage, // 3. Logar
    (req: Request, res: Response) => {
        // 4. Processar
        const { message } = req.body.validated

        setTimeout(() => {
            const reply = generateBotReply(message)

            res.json({
                reply,
                timestamp: new Date().toISOString(),
                messageId: generateMessageId(),
                status: "success",
            })
        }, 500 + Math.random() * 1000)
    }
)
```

---

## 📊 Comparação de Abordagens

| Aspecto                  | Zod          | Validação Manual | Middleware |
| ------------------------ | ------------ | ---------------- | ---------- |
| **Complexidade**         | Baixa        | Média            | Média      |
| **Dependências**         | 1 biblioteca | Nenhuma          | Nenhuma    |
| **Type Safety**          | ⭐⭐⭐⭐⭐   | ⭐⭐⭐           | ⭐⭐⭐     |
| **Manutenibilidade**     | ⭐⭐⭐⭐⭐   | ⭐⭐⭐           | ⭐⭐⭐⭐   |
| **Reutilização**         | ⭐⭐⭐⭐⭐   | ⭐⭐⭐           | ⭐⭐⭐⭐⭐ |
| **Performance**          | ⭐⭐⭐⭐     | ⭐⭐⭐⭐⭐       | ⭐⭐⭐⭐   |
| **Mensagens de Erro**    | Automáticas  | Manuais          | Manuais    |
| **Curva de Aprendizado** | Baixa        | Nenhuma          | Baixa      |

---

## 🎯 Recomendação

### Para Projetos Pequenos/Médios

**Use Zod** - Melhor custo-benefício entre simplicidade e robustez.

### Para Projetos Grandes

**Use Middlewares + Zod** - Máxima modularidade e reutilização.

### Para Projetos Sem Dependências

**Use Validação Manual** - Controle total sem bibliotecas externas.

---

## 🚀 Próximos Passos

1. **Testes Unitários**: Adicionar testes para validações
2. **Rate Limiting**: Prevenir spam de mensagens
3. **Autenticação**: Validar tokens JWT
4. **Logs Estruturados**: Usar Winston ou Pino
5. **Banco de Dados**: Persistir mensagens
6. **WebSocket**: Chat em tempo real

---

## 📚 Recursos Adicionais

-   [Zod Documentation](https://zod.dev/)
-   [Express Best Practices](https://expressjs.com/en/advanced/best-practice-security.html)
-   [OWASP Input Validation](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
-   [TypeScript Handbook](https://www.typescriptlang.org/docs/)

---

**Desenvolvido em:** 24 de Outubro de 2025  
**Versão:** 1.0.0
