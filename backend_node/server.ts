import express, { Request, Response } from "express"
import cors from "cors"
import swaggerUi from "swagger-ui-express"
import swaggerJsdoc from "swagger-jsdoc"

const app = express()
const PORT = 3001

// Configuração do Swagger
const swaggerOptions = {
    definition: {
        openapi: "3.0.0",
        info: {
            title: "Chat Bot API",
            version: "1.0.0",
            description: "API para chatbot com respostas automáticas",
            contact: {
                name: "Suporte API",
                email: "suporte@chat.com",
            },
        },
        servers: [
            {
                url: `http://localhost:${PORT}`,
                description: "Servidor de Desenvolvimento",
            },
        ],
        tags: [
            {
                name: "Chat",
                description: "Endpoints relacionados ao chat",
            },
            {
                name: "Health",
                description: "Endpoints de saúde do sistema",
            },
        ],
    },
    apis: ["./server.ts"], // Caminho para os arquivos com anotações
}

const swaggerSpec = swaggerJsdoc(swaggerOptions)

// Middleware
app.use(cors())
app.use(express.json())

// Rota do Swagger
app.use(
    "/api-docs",
    swaggerUi.serve,
    swaggerUi.setup(swaggerSpec, {
        customCss: ".swagger-ui .topbar { display: none }",
        customSiteTitle: "Chat Bot API Docs",
    })
)

// Respostas automáticas do bot
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

/**
 * @swagger
 * /:
 *   get:
 *     summary: Verifica se o servidor está rodando
 *     tags: [Health]
 *     responses:
 *       200:
 *         description: Servidor está ativo
 *         content:
 *           text/plain:
 *             schema:
 *               type: string
 *               example: "Servidor do Chatbot está rodando!"
 */
app.get("/", (req: Request, res: Response) => {
    res.send("Servidor do Chatbot está rodando!")
})

/**
 * @swagger
 * /api/chat:
 *   post:
 *     summary: Envia uma mensagem para o chatbot
 *     tags: [Chat]
 *     description: Recebe uma mensagem do usuário e retorna uma resposta automática do bot
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - message
 *             properties:
 *               message:
 *                 type: string
 *                 description: Mensagem do usuário
 *                 example: "Olá, como vai?"
 *                 minLength: 1
 *                 maxLength: 1000
 *               userId:
 *                 type: string
 *                 description: ID do usuário (opcional)
 *                 example: "user123"
 *     responses:
 *       200:
 *         description: Resposta do chatbot
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 reply:
 *                   type: string
 *                   description: Resposta do bot
 *                   example: "Olá! Como posso ajudar você hoje? 😊"
 *                 timestamp:
 *                   type: string
 *                   format: date-time
 *                   description: Timestamp da resposta
 *                   example: "2025-10-24T10:30:00.000Z"
 *       400:
 *         description: Mensagem inválida ou ausente
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 error:
 *                   type: string
 *                   example: "Mensagem é obrigatória"
 */
// Rota de chat
app.post("/api/chat", (req: Request, res: Response) => {
    const { message } = req.body

    if (!message) {
        return res.status(400).json({ error: "Mensagem é obrigatória" })
    }

    console.log(`Mensagem recebida: ${message}`)

    // Simula um pequeno delay para parecer mais real
    setTimeout(() => {
        // Seleciona uma resposta aleatória
        const randomResponse =
            botResponses[Math.floor(Math.random() * botResponses.length)]

        // Adiciona contexto baseado na mensagem do usuário
        let reply = randomResponse

        if (
            message.toLowerCase().includes("olá") ||
            message.toLowerCase().includes("oi")
        ) {
            reply = "Olá! Como posso ajudar você hoje? 😊"
        } else if (message.toLowerCase().includes("como vai")) {
            reply =
                "Estou muito bem, obrigado por perguntar! E você, como está?"
        } else if (
            message.toLowerCase().includes("tchau") ||
            message.toLowerCase().includes("adeus")
        ) {
            reply = "Até logo! Foi um prazer conversar com você! 👋"
        } else if (message.toLowerCase().includes("ajuda")) {
            reply = "Claro! Estou aqui para ajudar. O que você precisa?"
        } else if (message.toLowerCase().includes("?")) {
            reply = `Boa pergunta! Sobre "${message}", eu diria que é um tópico interessante para explorarmos.`
        }

        res.json({
            reply,
            timestamp: new Date().toISOString(),
        })
    }, 500 + Math.random() * 1000) // Delay entre 500ms e 1500ms
})

/**
 * @swagger
 * /health:
 *   get:
 *     summary: Verifica o status de saúde do servidor
 *     tags: [Health]
 *     description: Retorna o status de saúde da aplicação
 *     responses:
 *       200:
 *         description: Servidor está saudável
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 status:
 *                   type: string
 *                   example: "ok"
 *                 message:
 *                   type: string
 *                   example: "Servidor está funcionando!"
 */
// Rota de health check
app.get("/health", (req: Request, res: Response) => {
    res.json({ status: "ok", message: "Servidor está funcionando!" })
})

// Iniciar servidor
app.listen(PORT, () => {
    console.log(`🚀 Servidor rodando em http://localhost:${PORT}`)
    console.log(`📡 API disponível em http://localhost:${PORT}/api/chat`)
    console.log(`📚 Documentação Swagger em http://localhost:${PORT}/api-docs`)
})
