"""
Testes para validação de mensagens
Execute: poetry run pytest test_validation.py -v
"""

import pytest
from fastapi.testclient import TestClient
from main import app
from schemas import ChatRequest
from pydantic import ValidationError

client = TestClient(app)


class TestChatValidation:
    """Testes de validação do endpoint /api/chat"""
    
    def test_mensagem_valida(self):
        """✅ Teste: Mensagem válida deve ser aceita"""
        response = client.post(
            "/api/chat",
            json={"message": "Olá, como você está?"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "reply" in data
        assert "timestamp" in data
        assert data["message_length"] > 0
    
    def test_mensagem_vazia(self):
        """❌ Teste: Mensagem vazia deve ser rejeitada"""
        response = client.post(
            "/api/chat",
            json={"message": ""}
        )
        assert response.status_code == 422  # Unprocessable Entity
    
    def test_mensagem_apenas_espacos(self):
        """❌ Teste: Mensagem com apenas espaços deve ser rejeitada"""
        response = client.post(
            "/api/chat",
            json={"message": "    "}
        )
        assert response.status_code == 422
    
    def test_mensagem_sem_campo(self):
        """❌ Teste: Requisição sem campo 'message' deve ser rejeitada"""
        response = client.post(
            "/api/chat",
            json={}
        )
        assert response.status_code == 422
    
    def test_mensagem_apenas_pontuacao(self):
        """❌ Teste: Mensagem com apenas pontuação deve ser rejeitada"""
        response = client.post(
            "/api/chat",
            json={"message": "!!!!???"}
        )
        assert response.status_code == 422
    
    def test_mensagem_muito_longa(self):
        """❌ Teste: Mensagem maior que 1000 caracteres deve ser rejeitada"""
        long_message = "a" * 1001
        response = client.post(
            "/api/chat",
            json={"message": long_message}
        )
        assert response.status_code == 422
    
    def test_mensagem_com_espacos_extras(self):
        """✅ Teste: Mensagem com espaços extras deve ser limpa"""
        response = client.post(
            "/api/chat",
            json={"message": "  Olá  mundo  "}
        )
        assert response.status_code == 200
    
    def test_mensagem_com_emojis(self):
        """✅ Teste: Mensagem com emojis deve ser aceita"""
        response = client.post(
            "/api/chat",
            json={"message": "Olá! 😊🎉"}
        )
        assert response.status_code == 200
    
    def test_mensagem_com_numeros(self):
        """✅ Teste: Mensagem com números deve ser aceita"""
        response = client.post(
            "/api/chat",
            json={"message": "Tenho 25 anos"}
        )
        assert response.status_code == 200
    
    def test_mensagem_com_caracteres_especiais(self):
        """✅ Teste: Mensagem com caracteres especiais deve ser aceita"""
        response = client.post(
            "/api/chat",
            json={"message": "E-mail: teste@exemplo.com"}
        )
        assert response.status_code == 200
    
    def test_user_id_opcional(self):
        """✅ Teste: user_id é opcional"""
        response = client.post(
            "/api/chat",
            json={
                "message": "Olá",
                "user_id": "user123"
            }
        )
        assert response.status_code == 200
    
    def test_resposta_contem_metadata(self):
        """✅ Teste: Resposta deve conter metadata completo"""
        response = client.post(
            "/api/chat",
            json={"message": "Teste"}
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verifica campos obrigatórios
        assert "reply" in data
        assert "timestamp" in data
        assert "message_length" in data
        assert "processing_time" in data
        
        # Verifica tipos
        assert isinstance(data["reply"], str)
        assert isinstance(data["timestamp"], str)
        assert isinstance(data["message_length"], int)
        assert isinstance(data["processing_time"], float)
        
        # Verifica valores
        assert len(data["reply"]) > 0
        assert data["message_length"] == 5  # len("Teste")
        assert data["processing_time"] > 0


class TestChatRequestModel:
    """Testes diretos do modelo Pydantic"""
    
    def test_modelo_valido(self):
        """✅ Teste: Modelo com dados válidos"""
        request = ChatRequest(message="Olá")
        assert request.message == "Olá"
    
    def test_modelo_com_espacos(self):
        """✅ Teste: Modelo deve limpar espaços"""
        request = ChatRequest(message="  Olá  ")
        assert request.message == "Olá"  # Espaços removidos
    
    def test_modelo_mensagem_vazia(self):
        """❌ Teste: Modelo deve rejeitar mensagem vazia"""
        with pytest.raises(ValidationError):
            ChatRequest(message="")
    
    def test_modelo_apenas_espacos(self):
        """❌ Teste: Modelo deve rejeitar apenas espaços"""
        with pytest.raises(ValidationError):
            ChatRequest(message="   ")
    
    def test_modelo_apenas_pontuacao(self):
        """❌ Teste: Modelo deve rejeitar apenas pontuação"""
        with pytest.raises(ValidationError):
            ChatRequest(message="!!!!!")
    
    def test_modelo_muito_longo(self):
        """❌ Teste: Modelo deve rejeitar mensagem muito longa"""
        with pytest.raises(ValidationError):
            ChatRequest(message="a" * 1001)


class TestHealthEndpoint:
    """Testes do endpoint de health check"""
    
    def test_health_check(self):
        """✅ Teste: Health check deve retornar status ok"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "message" in data


class TestRootEndpoint:
    """Testes do endpoint raiz"""
    
    def test_root(self):
        """✅ Teste: Endpoint raiz deve responder"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data


# ============================================================================
# TESTES DE RESPOSTAS CONTEXTUAIS
# ============================================================================

class TestContextualResponses:
    """Testes das respostas contextuais do bot"""
    
    def test_resposta_ola(self):
        """✅ Teste: Mensagem com 'olá' deve ter resposta específica"""
        response = client.post(
            "/api/chat",
            json={"message": "Olá!"}
        )
        data = response.json()
        assert "Olá!" in data["reply"]
        assert "😊" in data["reply"]
    
    def test_resposta_como_vai(self):
        """✅ Teste: Mensagem com 'como vai' deve ter resposta específica"""
        response = client.post(
            "/api/chat",
            json={"message": "Como vai você?"}
        )
        data = response.json()
        assert "bem" in data["reply"].lower()
    
    def test_resposta_tchau(self):
        """✅ Teste: Mensagem com 'tchau' deve ter resposta de despedida"""
        response = client.post(
            "/api/chat",
            json={"message": "Tchau!"}
        )
        data = response.json()
        assert "logo" in data["reply"].lower() or "prazer" in data["reply"].lower()
    
    def test_resposta_ajuda(self):
        """✅ Teste: Mensagem com 'ajuda' deve oferecer ajuda"""
        response = client.post(
            "/api/chat",
            json={"message": "Preciso de ajuda"}
        )
        data = response.json()
        assert "ajuda" in data["reply"].lower()
    
    def test_resposta_pergunta(self):
        """✅ Teste: Mensagem com '?' deve reconhecer pergunta"""
        response = client.post(
            "/api/chat",
            json={"message": "Qual é o seu nome?"}
        )
        data = response.json()
        assert "pergunta" in data["reply"].lower() or "tópico" in data["reply"].lower()


# ============================================================================
# COMANDOS PARA EXECUTAR OS TESTES
# ============================================================================

"""
# Executar todos os testes
poetry run pytest test_validation.py -v

# Executar testes de uma classe específica
poetry run pytest test_validation.py::TestChatValidation -v

# Executar um teste específico
poetry run pytest test_validation.py::TestChatValidation::test_mensagem_valida -v

# Executar com coverage
poetry run pytest test_validation.py --cov=main --cov-report=html

# Executar com output detalhado
poetry run pytest test_validation.py -vv -s
"""
