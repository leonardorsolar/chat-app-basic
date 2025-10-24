import express, { Request, Response } from "express"
import cors from "cors"

const app = express()
const PORT = 3001

// Middleware
app.use(cors())
app.use(express.json())

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

app.get("/", (req: Request, res: Response) => {
    res.send("Servidor do Chatbot está rodando!")
})

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

// Rota de health check
app.get("/health", (req: Request, res: Response) => {
    res.json({ status: "ok", message: "Servidor está funcionando!" })
})

// Iniciar servidor
app.listen(PORT, () => {
    console.log(`🚀 Servidor rodando em http://localhost:${PORT}`)
    console.log(`📡 API disponível em http://localhost:${PORT}/api/chat`)
})
