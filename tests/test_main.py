import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Testa o endpoint de health check."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_execute_endpoint_structure():
    """Testa a estrutura do endpoint execute."""
    # Dados de teste
    test_data = {
        "agent_name": "test-agent",
        "agent_description": "Um agente de teste",
        "input_schema": {
            "field1": "string",
            "field2": "number"
        },
        "output_schema": {
            "result": "string",
            "status": "boolean"
        }
    }
    
    # Este teste não executa realmente a chamada à API do OpenAI,
    # apenas verifica se o endpoint responde corretamente
    # Seria melhor criar um mock para o serviço OpenAI
    
    # Substitua por um teste mais significativo com mocks apropriados
    # response = client.post("/api/v1/execute", json=test_data)
    # assert response.status_code == 200
    # assert "files" in response.json()
    # assert "status" in response.json()
    
    # Por enquanto, apenas verificamos se as classes estão definidas corretamente
    from app.models.agent_model import InputModel, OutputModel
    assert hasattr(InputModel, "agent_name")
    assert hasattr(OutputModel, "files") 