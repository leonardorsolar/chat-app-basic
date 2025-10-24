# 📝 Guia Completo de Logging com Python Logger

## 🎯 O que é Logging?

Logging é o processo de registrar eventos que acontecem durante a execução de uma aplicação. É essencial para:

-   🐛 **Debug**: Encontrar e corrigir problemas
-   📊 **Monitoramento**: Acompanhar o comportamento da aplicação
-   🔍 **Auditoria**: Rastrear ações e eventos importantes
-   📈 **Análise**: Entender padrões de uso

---

## Como Usar (Resumo):

# 1. Rodar aplicação (cria debug.log automaticamente)

poetry run python main.py

# 2. Enviar mensagens (via curl, Swagger, ou frontend)

curl -X POST http://localhost:3002/api/chat \
 -H "Content-Type: application/json" \
 -d '{"message": "olá"}'

# 3. Analisar logs

poetry run python analyze_logs.py debug.log

## Se ainda não funcionar:

# Opção 1: Python direto (sem poetry)

python analyze_logs.py debug.log

# Opção 2: Python3

python3 analyze_logs.py debug.log

# Opção 3: Verificar se arquivo existe

ls -lh debug.log
cat debug.log

## 🚫 Por que NÃO usar `print()`?

### ❌ Problemas com `print()`:

```python
# ❌ RUIM
print("Mensagem recebida:", message)
```

**Desvantagens:**

1. ❌ Sem níveis de severidade (info, warning, error)
2. ❌ Sem timestamps automáticos
3. ❌ Difícil de desabilitar em produção
4. ❌ Não pode ser direcionado para arquivos
5. ❌ Sem formatação consistente
6. ❌ Mistura com output normal da aplicação

### ✅ Vantagens do Logger:

```python
# ✅ BOM
logger.info("📨 Mensagem recebida: %s", message)
```

**Vantagens:**

1. ✅ Níveis de severidade (DEBUG, INFO, WARNING, ERROR, CRITICAL)
2. ✅ Timestamps automáticos
3. ✅ Fácil de configurar e desabilitar
4. ✅ Pode ser enviado para arquivo, console, servidores remotos
5. ✅ Formatação consistente e configurável
6. ✅ Filtragem por módulo/componente

---

## 🏗️ Como o Logger foi Configurado na Nossa Aplicação

### Código em `main.py`:

```python
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

### 📖 Explicação Linha por Linha:

#### 1. **Import do módulo**

```python
import logging
```

Importa o módulo de logging padrão do Python (não precisa instalar nada extra).

#### 2. **Configuração básica**

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

**Parâmetros:**

-   **`level=logging.INFO`**: Define o nível mínimo de log

    -   `DEBUG`: Informações detalhadas para diagnóstico
    -   `INFO`: Confirmação de que as coisas estão funcionando ✅ **USADO NA APP**
    -   `WARNING`: Algo inesperado, mas ainda funciona
    -   `ERROR`: Erro sério, função não executou
    -   `CRITICAL`: Erro grave, aplicação pode parar

-   **`format='...'`**: Define como as mensagens aparecerão
    -   `%(asctime)s`: Timestamp (data e hora)
    -   `%(name)s`: Nome do logger (geralmente o módulo)
    -   `%(levelname)s`: Nível do log (INFO, ERROR, etc)
    -   `%(message)s`: A mensagem em si

#### 3. **Criação do logger**

```python
logger = logging.getLogger(__name__)
```

-   `__name__`: Nome do módulo atual (ex: `__main__`, `main`, etc)
-   Cria um logger específico para este arquivo
-   Permite filtrar logs por módulo

---

## 💡 Como Usamos o Logger na Aplicação

### 1️⃣ **Log de Entrada de Mensagem**

```python
logger.info(f"📨 Mensagem recebida: '{request.message}' | User ID: {request.user_id}")
```

**O que acontece:**

```
2025-10-24 14:30:15,123 - __main__ - INFO - 📨 Mensagem recebida: 'Olá, como vai?' | User ID: user123
```

**Por que usamos:**

-   ✅ Registra toda mensagem que chega
-   ✅ Ajuda a debugar problemas de comunicação
-   ✅ Permite auditoria de conversas
-   ✅ Rastreamento de usuários

### 2️⃣ **Log de Saída de Resposta**

```python
logger.info(f"📤 Resposta enviada: '{reply[:50]}...' | Tempo: {processing_time:.3f}s")
```

**O que acontece:**

```
2025-10-24 14:30:16,456 - __main__ - INFO - 📤 Resposta enviada: 'Olá! Como posso ajudar você hoje? 😊' | Tempo: 0.875s
```

**Por que usamos:**

-   ✅ Registra a resposta gerada
-   ✅ Monitora tempo de processamento
-   ✅ Detecta respostas muito lentas
-   ✅ Completa o ciclo de log (entrada + saída)

---

## 🎨 Diferentes Níveis de Log

### Exemplo Completo:

```python
import logging

logger = logging.getLogger(__name__)

# 🔍 DEBUG - Informações detalhadas para diagnóstico
logger.debug("Iniciando processamento da mensagem")
logger.debug(f"Mensagem original: {raw_message}")

# ℹ️ INFO - Confirmação que tudo está funcionando
logger.info("📨 Mensagem recebida com sucesso")
logger.info("📤 Resposta enviada ao usuário")

# ⚠️ WARNING - Algo inesperado, mas não crítico
logger.warning("Mensagem muito longa detectada (500 chars)")
logger.warning("Taxa de requisições alta para o usuário X")

# ❌ ERROR - Erro que impede uma operação
logger.error("Falha ao conectar com o banco de dados")
logger.error(f"Erro ao processar mensagem: {error}")

# 🔥 CRITICAL - Erro grave que pode parar a aplicação
logger.critical("Sistema de autenticação falhou completamente")
logger.critical("Memória RAM esgotada")
```

### Quando Usar Cada Nível:

| Nível        | Quando Usar                                      | Exemplo                                     |
| ------------ | ------------------------------------------------ | ------------------------------------------- |
| **DEBUG**    | Desenvolvimento, informações técnicas detalhadas | Valores de variáveis, fluxo de execução     |
| **INFO**     | ✅ Eventos normais importantes                   | Requisições recebidas, operações concluídas |
| **WARNING**  | Situações inesperadas mas não críticas           | Retry de operação, dados suspeitos          |
| **ERROR**    | Erros que impedem uma operação                   | Falha de conexão, arquivo não encontrado    |
| **CRITICAL** | Falhas graves do sistema                         | Sistema indisponível, corrupção de dados    |

---

## 🔧 Configurações Avançadas

### 1. **Log para Arquivo**

```python
import logging
from logging.handlers import RotatingFileHandler

# Cria handler para arquivo
file_handler = RotatingFileHandler(
    'chatbot.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5            # Mantém 5 arquivos
)

# Define formato
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)

# Adiciona ao logger
logger = logging.getLogger(__name__)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
```

### 2. **Log para Console E Arquivo**

```python
import logging
import sys

# Handler para console (stdout)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter(
    '%(levelname)s - %(message)s'
)
console_handler.setFormatter(console_formatter)

# Handler para arquivo
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(file_formatter)

# Configura logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
logger.addHandler(file_handler)
```

### 3. **Log Estruturado (JSON)**

```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        return json.dumps(log_data)

# Usar formatter
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Resultado:
# {"timestamp": "2025-10-24T14:30:15.123", "level": "INFO", ...}
```

---

## 🎯 Melhores Práticas de Logging

### ✅ DO (Faça):

#### 1. **Use f-strings ou % para interpolação**

```python
# ✅ BOM - Eficiente
logger.info("Mensagem de %s processada em %.2fs", user, time)

# ✅ TAMBÉM BOM - Mais legível
logger.info(f"Mensagem de {user} processada em {time:.2f}s")
```

#### 2. **Use emojis para identificação rápida**

```python
logger.info("📨 Mensagem recebida")
logger.info("📤 Resposta enviada")
logger.warning("⚠️ Taxa limite atingida")
logger.error("❌ Falha ao processar")
```

#### 3. **Inclua contexto relevante**

```python
# ✅ BOM - Com contexto
logger.info("Usuário %s enviou mensagem de %d chars", user_id, len(msg))

# ❌ RUIM - Sem contexto
logger.info("Mensagem enviada")
```

#### 4. **Use try/except com logging**

```python
try:
    result = process_message(message)
    logger.info("✅ Mensagem processada com sucesso")
except ValueError as e:
    logger.error("❌ Erro de validação: %s", e)
except Exception as e:
    logger.exception("🔥 Erro inesperado ao processar mensagem")
    # logger.exception() inclui stack trace automaticamente
```

#### 5. **Configure diferentes níveis por ambiente**

```python
import os

# Desenvolvimento: DEBUG
# Produção: INFO ou WARNING
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### ❌ DON'T (Não Faça):

#### 1. **Não logue dados sensíveis**

```python
# ❌ MUITO RUIM - Expõe senha
logger.info(f"Login: {username} / {password}")

# ✅ BOM - Não expõe senha
logger.info(f"Tentativa de login: {username}")
```

#### 2. **Não logue em loops intensos**

```python
# ❌ RUIM - Muito log
for item in large_list:
    logger.debug(f"Processando {item}")

# ✅ BOM - Log resumido
logger.debug(f"Processando {len(large_list)} items")
```

#### 3. **Não use apenas print()**

```python
# ❌ RUIM
print("Erro ao processar")

# ✅ BOM
logger.error("❌ Erro ao processar mensagem")
```

---

## 📊 Exemplo Real: Fluxo Completo com Logging

```python
import logging
import time
from typing import Optional

logger = logging.getLogger(__name__)

async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """Endpoint com logging completo"""

    # 1. Log de início
    request_id = generate_request_id()
    start_time = time.time()

    logger.info(
        "📨 [%s] Nova requisição | User: %s | Message: '%s' (%d chars)",
        request_id,
        request.user_id or "anonymous",
        request.message[:50],  # Primeiros 50 chars
        len(request.message)
    )

    try:
        # 2. Processar mensagem
        logger.debug("[%s] Iniciando processamento", request_id)

        reply = await process_message(request.message)

        # 3. Log de sucesso
        processing_time = time.time() - start_time

        logger.info(
            "📤 [%s] Resposta enviada | Reply: '%s' | Tempo: %.3fs",
            request_id,
            reply[:50],
            processing_time
        )

        # 4. Alerta se muito lento
        if processing_time > 2.0:
            logger.warning(
                "⚠️ [%s] Processamento lento detectado: %.3fs",
                request_id,
                processing_time
            )

        return ChatResponse(
            reply=reply,
            timestamp=datetime.utcnow().isoformat(),
            processing_time=processing_time
        )

    except ValidationError as e:
        # 5. Log de erro de validação
        logger.warning(
            "⚠️ [%s] Erro de validação: %s",
            request_id,
            str(e)
        )
        raise

    except Exception as e:
        # 6. Log de erro crítico
        logger.exception(
            "🔥 [%s] Erro inesperado ao processar mensagem",
            request_id
        )
        raise

    finally:
        # 7. Log final (sempre executa)
        total_time = time.time() - start_time
        logger.debug(
            "[%s] Requisição finalizada | Tempo total: %.3fs",
            request_id,
            total_time
        )
```

### Output no Console:

```
2025-10-24 14:30:15,123 - __main__ - INFO - 📨 [req-abc123] Nova requisição | User: user789 | Message: 'Olá, como você está?' (20 chars)
2025-10-24 14:30:15,124 - __main__ - DEBUG - [req-abc123] Iniciando processamento
2025-10-24 14:30:16,001 - __main__ - INFO - 📤 [req-abc123] Resposta enviada | Reply: 'Olá! Como posso ajudar você hoje? 😊' | Tempo: 0.878s
2025-10-24 14:30:16,002 - __main__ - DEBUG - [req-abc123] Requisição finalizada | Tempo total: 0.879s
```

---

## 🔍 Análise de Logs

### Comandos Úteis (Linux/Mac):

```bash
# Ver logs em tempo real
tail -f app.log

# Buscar erros
grep "ERROR" app.log

# Contar mensagens por nível
grep -c "INFO" app.log
grep -c "ERROR" app.log

# Ver últimas 100 linhas
tail -n 100 app.log

# Filtrar por timestamp
grep "2025-10-24 14:" app.log

# Buscar por usuário específico
grep "User: user789" app.log
```

---

## 🚀 Implementação na Nossa Aplicação

### Código Atual em `main.py`:

```python
# Configuração inicial
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Uso no endpoint
@app.post("/api/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    # Log de entrada
    logger.info(
        f"📨 Mensagem recebida: '{request.message}' | User ID: {request.user_id}"
    )

    # ... processar ...

    # Log de saída
    logger.info(
        f"📤 Resposta enviada: '{reply[:50]}...' | Tempo: {processing_time:.3f}s"
    )
```

### Benefícios:

1. ✅ **Rastreabilidade**: Toda interação é registrada
2. ✅ **Debug**: Fácil identificar problemas
3. ✅ **Monitoramento**: Acompanhar performance
4. ✅ **Auditoria**: Histórico completo
5. ✅ **Análise**: Entender padrões de uso

---

## 📚 Recursos Adicionais

### Documentação Oficial:

-   [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
-   [Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)

### Bibliotecas Avançadas:

-   **Loguru**: Logging mais simples e bonito
-   **Structlog**: Logging estruturado
-   **Python-json-logger**: Logs em JSON

### Ferramentas de Análise:

-   **ELK Stack** (Elasticsearch, Logstash, Kibana)
-   **Grafana Loki**: Para logs
-   **Datadog**: Monitoramento completo
-   **Sentry**: Para rastreamento de erros

---

## 🎓 Resumo

### Por que Usamos Logger:

✅ Registrar eventos importantes  
✅ Facilitar debug e troubleshooting  
✅ Monitorar performance  
✅ Auditar ações de usuários  
✅ Analisar padrões de uso

### Como Usamos:

✅ `logger.info()` para eventos normais  
✅ `logger.warning()` para situações inesperadas  
✅ `logger.error()` para erros  
✅ Formato consistente com timestamps  
✅ Emojis para identificação visual

### Onde Usamos:

✅ Entrada de requisições (📨)  
✅ Saída de respostas (📤)  
✅ Erros e exceções (❌)  
✅ Eventos importantes do sistema

**Logger é essencial para aplicações profissionais em produção!** 🚀

# 🐛 Guia Completo: Como Analisar Debug com Logger

## 📋 Índice

1. [Configurando o Modo Debug](#1-configurando-o-modo-debug)
2. [Visualizando Logs em Tempo Real](#2-visualizando-logs-em-tempo-real)
3. [Analisando Logs Salvos](#3-analisando-logs-salvos)
4. [Ferramentas de Debug](#4-ferramentas-de-debug)
5. [Cenários Práticos](#5-cenários-práticos)
6. [Troubleshooting Comum](#6-troubleshooting-comum)

---

## 1. 🔧 Configurando o Modo Debug

### 1.1. Habilitando Nível DEBUG no `main.py`

```python
# filepath: /home/leonardo/Documents/00 Empresa AES/Chatclone/chat-app-basic/backend_python/main.py
import logging

# ANTES (apenas INFO)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# DEPOIS (com DEBUG)
logging.basicConfig(
    level=logging.DEBUG,  # 👈 Mudança aqui
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

### 1.2. Configuração Avançada com Arquivo

```python
# filepath: /home/leonardo/Documents/00 Empresa AES/Chatclone/chat-app-basic/backend_python/main.py
import logging
from logging.handlers import RotatingFileHandler
import sys

# Criar logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Formato detalhado
formatter = logging.Formatter(
    '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Handler para console (INFO e acima)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Handler para arquivo (DEBUG e acima)
file_handler = RotatingFileHandler(
    'debug.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Adicionar handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)
```

### 1.3. Adicionando Logs de Debug no Código

```python
# filepath: /home/leonardo/Documents/00 Empresa AES/Chatclone/chat-app-basic/backend_python/main.py
@app.post("/api/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    start_time = time.time()

    # 🐛 DEBUG: Log detalhado da requisição
    logger.debug(f"🔍 Request completo: {request.model_dump()}")
    logger.debug(f"🔍 Headers recebidos: {request.headers if hasattr(request, 'headers') else 'N/A'}")

    # 📨 INFO: Log de mensagem recebida
    logger.info(f"📨 Mensagem recebida: '{request.message}' | User ID: {request.user_id}")

    message = request.message
    message_lower = message.lower()

    # 🐛 DEBUG: Log do processamento
    logger.debug(f"🔍 Mensagem normalizada: '{message_lower}'")

    # Delay
    delay = 0.5 + random.random()
    logger.debug(f"🔍 Delay calculado: {delay:.3f}s")
    await asyncio.sleep(delay)

    # Seleciona resposta
    reply = random.choice(BOT_RESPONSES)
    logger.debug(f"🔍 Resposta inicial selecionada: '{reply}'")

    # Contexto
    if "olá" in message_lower or "oi" in message_lower:
        reply = "Olá! Como posso ajudar você hoje? 😊"
        logger.debug(f"🔍 Contexto detectado: SAUDAÇÃO")
    elif "ajuda" in message_lower:
        reply = "Claro! Estou aqui para ajudar. O que você precisa?"
        logger.debug(f"🔍 Contexto detectado: AJUDA")

    processing_time = time.time() - start_time

    # 📤 INFO: Log de resposta enviada
    logger.info(f"📤 Resposta enviada: '{reply[:50]}...' | Tempo: {processing_time:.3f}s")

    # 🐛 DEBUG: Log da resposta completa
    logger.debug(f"🔍 Response completo: reply='{reply}', length={len(message)}, time={processing_time}")

    return ChatResponse(
        reply=reply,
        timestamp=datetime.utcnow().isoformat() + "Z",
        message_length=len(message),
        processing_time=round(processing_time, 3)
    )
```

---

## 2. 👀 Visualizando Logs em Tempo Real

### 2.1. No Terminal (Simples)

```bash
# Rodar a aplicação
poetry run python main.py

# Você verá:
2025-10-24 15:30:45 | INFO     | __main__:86 | 📨 Mensagem recebida: 'olá' | User ID: None
2025-10-24 15:30:46 | INFO     | __main__:118 | 📤 Resposta enviada: 'Olá! Como posso ajudar você hoje? 😊' | Tempo: 0.892s
```

### 2.2. Acompanhando Arquivo de Log

```bash
# Terminal 1: Rodar aplicação
poetry run python main.py

# Terminal 2: Acompanhar logs em tempo real
tail -f debug.log

# Ver apenas logs de DEBUG
tail -f debug.log | grep DEBUG

# Ver apenas logs de INFO e acima
tail -f debug.log | grep -E "INFO|WARNING|ERROR"
```

### 2.3. Colorindo Logs (Opcional)

```bash
# Instalar colorlog
poetry add colorlog

# Modificar main.py
import colorlog

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
))
```

---

## 3. 🔍 Analisando Logs Salvos

### 3.1. Comandos Básicos

```bash
# Ver últimas 50 linhas
tail -n 50 debug.log

# Ver primeiras 50 linhas
head -n 50 debug.log

# Ver arquivo inteiro
cat debug.log

# Ver com paginação
less debug.log  # Use 'q' para sair
```

### 3.2. Buscando Padrões

```bash
# Buscar por palavra-chave
grep "Mensagem recebida" debug.log

# Buscar erros
grep "ERROR" debug.log

# Buscar por usuário específico
grep "User ID: user123" debug.log

# Buscar com contexto (2 linhas antes e depois)
grep -C 2 "ERROR" debug.log

# Buscar ignorando maiúsculas
grep -i "erro" debug.log

# Contar ocorrências
grep -c "Mensagem recebida" debug.log
```

### 3.3. Filtrando por Data/Hora

```bash
# Ver logs de hoje
grep "$(date +%Y-%m-%d)" debug.log

# Ver logs de uma hora específica
grep "2025-10-24 15:" debug.log

# Ver logs entre horários
awk '/2025-10-24 14:00/,/2025-10-24 15:00/' debug.log
```

### 3.4. Analisando Performance

```bash
# Ver todos os tempos de processamento
grep "Tempo:" debug.log

# Ver tempos > 1 segundo
grep "Tempo:" debug.log | awk -F'Tempo: ' '{print $2}' | awk '{if ($1 > 1.0) print}'

# Ver mensagens mais lentas
grep "Tempo:" debug.log | sort -t':' -k4 -rn | head -10
```

---

## 4. 🛠️ Ferramentas de Debug

### 4.1. Script de Análise Python

```python
# filepath: /home/leonardo/Documents/00 Empresa AES/Chatclone/chat-app-basic/backend_python/analyze_logs.py
"""
Script para analisar logs do chatbot
Usage: python analyze_logs.py debug.log
"""
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime

def analyze_log_file(filepath: str):
    """Analisa arquivo de log e gera estatísticas"""

    stats = {
        'total_messages': 0,
        'total_errors': 0,
        'total_warnings': 0,
        'processing_times': [],
        'message_lengths': [],
        'contexts': Counter(),
        'hourly_distribution': defaultdict(int)
    }

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            # Contar por nível
            if 'ERROR' in line:
                stats['total_errors'] += 1
            elif 'WARNING' in line:
                stats['total_warnings'] += 1

            # Mensagens recebidas
            if '📨 Mensagem recebida' in line:
                stats['total_messages'] += 1

                # Extrair timestamp para distribuição horária
                timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}):', line)
                if timestamp_match:
                    hour = timestamp_match.group(1)
                    stats['hourly_distribution'][hour] += 1

            # Tempos de processamento
            time_match = re.search(r'Tempo: (\d+\.\d+)s', line)
            if time_match:
                stats['processing_times'].append(float(time_match.group(1)))

            # Tamanho de mensagens
            length_match = re.search(r'length=(\d+)', line)
            if length_match:
                stats['message_lengths'].append(int(length_match.group(1)))

            # Contextos detectados
            context_match = re.search(r'Contexto detectado: (\w+)', line)
            if context_match:
                stats['contexts'][context_match.group(1)] += 1

    # Imprimir relatório
    print("\n" + "="*60)
    print("📊 RELATÓRIO DE ANÁLISE DE LOGS")
    print("="*60)

    print(f"\n📨 Total de Mensagens: {stats['total_messages']}")
    print(f"❌ Total de Erros: {stats['total_errors']}")
    print(f"⚠️  Total de Avisos: {stats['total_warnings']}")

    if stats['processing_times']:
        avg_time = sum(stats['processing_times']) / len(stats['processing_times'])
        min_time = min(stats['processing_times'])
        max_time = max(stats['processing_times'])

        print(f"\n⏱️  Tempos de Processamento:")
        print(f"   Média: {avg_time:.3f}s")
        print(f"   Mínimo: {min_time:.3f}s")
        print(f"   Máximo: {max_time:.3f}s")

    if stats['message_lengths']:
        avg_length = sum(stats['message_lengths']) / len(stats['message_lengths'])
        print(f"\n📏 Tamanho Médio de Mensagens: {avg_length:.1f} caracteres")

    if stats['contexts']:
        print(f"\n🎯 Contextos Detectados:")
        for context, count in stats['contexts'].most_common():
            print(f"   {context}: {count} vezes")

    if stats['hourly_distribution']:
        print(f"\n📅 Distribuição por Hora:")
        for hour in sorted(stats['hourly_distribution'].keys())[-10:]:  # Últimas 10 horas
            count = stats['hourly_distribution'][hour]
            bar = '█' * (count // 2)
            print(f"   {hour}: {bar} ({count})")

    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_logs.py <log_file>")
        sys.exit(1)

    analyze_log_file(sys.argv[1])
```

### 4.2. Usando o Script

```bash
# Analisar logs
poetry run python analyze_logs.py debug.log

# Saída esperada:
# ============================================================
# 📊 RELATÓRIO DE ANÁLISE DE LOGS
# ============================================================
#
# 📨 Total de Mensagens: 150
# ❌ Total de Erros: 2
# ⚠️  Total de Avisos: 5
#
# ⏱️  Tempos de Processamento:
#    Média: 0.892s
#    Mínimo: 0.501s
#    Máximo: 1.498s
#
# 📏 Tamanho Médio de Mensagens: 28.5 caracteres
#
# 🎯 Contextos Detectados:
#    SAUDAÇÃO: 45 vezes
#    AJUDA: 23 vezes
#
# 📅 Distribuição por Hora:
#    2025-10-24 14: ████████ (16)
#    2025-10-24 15: ██████████████ (28)
# ============================================================
```

---

## 5. 🎯 Cenários Práticos de Debug

### 5.1. Problema: Aplicação está lenta

```bash
# 1. Verificar tempos de processamento
grep "Tempo:" debug.log | tail -20

# 2. Encontrar requisições lentas (> 2s)
grep "Tempo:" debug.log | grep -E "Tempo: [2-9]\." | tail -10

# 3. Ver o que estava acontecendo antes
grep -B 5 "Tempo: 5.123s" debug.log
```

### 5.2. Problema: Usuário reportou erro

```bash
# 1. Buscar por User ID
grep "User ID: user123" debug.log

# 2. Ver todos os logs do usuário em contexto
grep -C 3 "User ID: user123" debug.log

# 3. Verificar se houve erros
grep "User ID: user123" debug.log | grep -i error
```

### 5.3. Problema: Resposta inesperada

```python
# Adicionar mais logs de debug
logger.debug(f"🔍 Variáveis no momento: message='{message}', reply='{reply}'")
logger.debug(f"🔍 Condições testadas: ola={('olá' in message_lower)}, ajuda={('ajuda' in message_lower)}")
```

```bash
# Verificar logs de debug
grep "🔍" debug.log | tail -20
```

### 5.4. Problema: Erro intermitente

```python
# Adicionar try/except com logging detalhado
try:
    reply = random.choice(BOT_RESPONSES)
    logger.debug(f"✅ Resposta selecionada com sucesso")
except Exception as e:
    logger.error(f"❌ Erro ao selecionar resposta: {e}", exc_info=True)
    reply = "Desculpe, ocorreu um erro."
```

---

## 6. 🔧 Troubleshooting Comum

### 6.1. Logs não aparecem

```python
# Verificar se o logger está configurado
import logging
print(logging.getLogger(__name__).level)  # Deve mostrar 10 (DEBUG) ou 20 (INFO)

# Forçar flush
import sys
sys.stdout.flush()
```

### 6.2. Arquivo de log não é criado

```python
# Verificar permissões
import os
print(os.access('.', os.W_OK))  # Deve retornar True

# Usar caminho absoluto
file_handler = RotatingFileHandler(
    '/tmp/debug.log',  # Caminho absoluto
    maxBytes=10*1024*1024,
    backupCount=5
)
```

### 6.3. Logs duplicados

```python
# Remover handlers antigos antes de adicionar novos
logger.handlers.clear()
logger.addHandler(console_handler)
logger.addHandler(file_handler)
```

### 6.4. Performance degradada por excesso de logs

```python
# Usar níveis diferentes por ambiente
import os

if os.getenv('ENV') == 'production':
    logger.setLevel(logging.INFO)
else:
    logger.setLevel(logging.DEBUG)
```

---

## 7. 📝 Checklist de Debug

### Antes de investigar um problema:

-   [ ] Logs estão habilitados no nível adequado (DEBUG)?
-   [ ] Arquivo de log está sendo gerado?
-   [ ] Você tem acesso de leitura ao arquivo?
-   [ ] O timestamp está correto?

### Durante a investigação:

-   [ ] Identificou o horário exato do problema?
-   [ ] Buscou por User ID ou mensagem específica?
-   [ ] Verificou logs antes e depois do erro?
-   [ ] Procurou por padrões repetitivos?

### Após resolver:

-   [ ] Adicionou logs para prevenir o problema no futuro?
-   [ ] Documentou a causa raiz?
-   [ ] Atualizou testes se necessário?

---

## 8. 🚀 Comandos Rápidos (Cheat Sheet)

```bash
# Ver logs em tempo real
tail -f debug.log

# Buscar erros
grep ERROR debug.log

# Últimas 100 linhas
tail -n 100 debug.log

# Contar mensagens de hoje
grep "$(date +%Y-%m-%d)" debug.log | grep "Mensagem recebida" | wc -l

# Ver apenas DEBUG
grep DEBUG debug.log | tail -20

# Buscar e colorir
grep --color=always "ERROR" debug.log

# Analisar estatísticas
poetry run python analyze_logs.py debug.log
```

---

## 📚 Referências

-   [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
-   [FastAPI Logging](https://fastapi.tiangolo.com/tutorial/logging/)
-   [Best Practices](https://betterstack.com/community/guides/logging/python/python-logging-best-practices/)

---

**Criado para o projeto Chatbot Backend API** 🤖
