from fastapi import APIRouter, HTTPException, Depends
from app.models.agent_model import InputModel, OutputModel, GeneratedFile
from typing import Dict, Any, List
import os
import json
import logging
from openai import OpenAI
from dotenv import load_dotenv

# Configurar logging
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

# Configurar o cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Mensagens do sistema para cada tipo de geração
CONTROLLER_SYSTEM_MESSAGE = """Você é um especialista em desenvolvimento de APIs com FastAPI. 
Sua tarefa é gerar um arquivo controller.py para um agente conforme as especificações.
O código deve ser bem estruturado, comentado e seguir as melhores práticas."""

TESTS_SYSTEM_MESSAGE = """Você é um especialista em testes de API com pytest. 
Sua tarefa é gerar um arquivo test_main.py para testar um agente conforme as especificações."""

README_SYSTEM_MESSAGE = """Você é um especialista em documentação de software. 
Sua tarefa é gerar um arquivo README.md para um agente conforme as especificações."""

PROMPT_SYSTEM_MESSAGE = """Você é um especialista em prompts para IA. 
Sua tarefa é gerar um arquivo de prompt detalhado para um agente conforme as especificações."""

router = APIRouter(prefix="/api/v1", tags=["agent"])

def validate_schema(schema: Dict) -> bool:
    """
    Valida se o schema fornecido é um schema JSON válido.
    """
    required_fields = ["type", "properties"]
    if not all(field in schema for field in required_fields):
        raise ValueError("Schema inválido: deve conter os campos 'type' e 'properties'")
    if schema["type"] != "object":
        raise ValueError("Schema inválido: o tipo deve ser 'object'")
    if not isinstance(schema["properties"], dict):
        raise ValueError("Schema inválido: 'properties' deve ser um objeto")
    return True

def generate_with_openai(system_message: str, prompt: str, max_tokens: int = 2000) -> str:
    """
    Função genérica para gerar conteúdo usando a OpenAI API.
    """
    try:
        logger.info(f"Gerando conteúdo com prompt de {len(prompt)} caracteres")
        response = client.chat.completions.create(
            model="gpt-4", 
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=max_tokens
        )
        content = response.choices[0].message.content.strip()
        logger.info(f"Conteúdo gerado com {len(content)} caracteres")
        return content
    except Exception as e:
        logger.error(f"Erro ao gerar conteúdo: {str(e)}")
        raise

def generate_controller(agent_name: str, agent_description: str, input_schema: Dict, output_schema: Dict, agent_prompt: str = None) -> str:
    """
    Gera o código do controller usando a OpenAI API.
    """
    prompt = f"""
    Crie um controller.py para um agente chamado '{agent_name}' que {agent_description}.
    
    O agente recebe os seguintes dados de entrada:
    {json.dumps(input_schema, indent=2)}
    
    E deve retornar:
    {json.dumps(output_schema, indent=2)}
    
    Requisitos:
    - Utilize FastAPI para criar um endpoint /execute que recebe o modelo de entrada e retorna o modelo de saída
    - Implemente a lógica de negócio necessária para processar os dados de entrada
    - Adicione tratamento de erros apropriado
    - Use docstrings para documentar o código
    - Não inclua imports desnecessários
    
    Retorne apenas o código, sem explicações adicionais.
    """
    
    if agent_prompt:
        prompt += f"\n\nInstruções adicionais: {agent_prompt}"
    
    try:
        return generate_with_openai(CONTROLLER_SYSTEM_MESSAGE, prompt, 2000)
    except Exception as e:
        raise Exception(f"Erro ao gerar controller: {str(e)}")

def generate_tests(agent_name: str, agent_description: str, input_schema: Dict, output_schema: Dict) -> str:
    """
    Gera o código de testes usando a OpenAI API.
    """
    prompt = f"""
    Crie um arquivo test_main.py para testar um agente chamado '{agent_name}' que {agent_description}.
    
    O agente recebe os seguintes dados de entrada:
    {json.dumps(input_schema, indent=2)}
    
    E retorna:
    {json.dumps(output_schema, indent=2)}
    
    Requisitos:
    - Utilize pytest e o TestClient do FastAPI
    - Teste o endpoint /health
    - Teste o endpoint /api/v1/execute com dados de exemplo
    - Valide o schema de saída
    - Use fixtures quando apropriado
    
    Retorne apenas o código, sem explicações adicionais.
    """
    
    try:
        return generate_with_openai(TESTS_SYSTEM_MESSAGE, prompt, 1500)
    except Exception as e:
        raise Exception(f"Erro ao gerar testes: {str(e)}")

def generate_readme(agent_name: str, agent_description: str, input_schema: Dict, output_schema: Dict) -> str:
    """
    Gera o README.md usando a OpenAI API.
    """
    prompt = f"""
    Crie um README.md para um agente chamado '{agent_name}' que {agent_description}.
    
    O agente recebe os seguintes dados de entrada:
    {json.dumps(input_schema, indent=2)}
    
    E retorna:
    {json.dumps(output_schema, indent=2)}
    
    Requisitos:
    - Título e descrição clara
    - Instruções de instalação
    - Instruções de uso com exemplos de entrada/saída
    - Explicação do endpoint
    - Use markdown adequadamente
    
    Retorne apenas o conteúdo do README, sem explicações adicionais.
    """
    
    try:
        return generate_with_openai(README_SYSTEM_MESSAGE, prompt, 1000)
    except Exception as e:
        raise Exception(f"Erro ao gerar README: {str(e)}")

def generate_prompt_file(agent_name: str, agent_description: str, input_schema: Dict, output_schema: Dict, agent_prompt: str = None) -> str:
    """
    Gera um arquivo de prompt para o agente usando a OpenAI API.
    """
    prompt = f"""
    Crie um arquivo de prompt para um agente chamado '{agent_name}' que {agent_description}.
    
    O agente recebe os seguintes dados de entrada:
    {json.dumps(input_schema, indent=2)}
    
    E retorna:
    {json.dumps(output_schema, indent=2)}
    
    O prompt deve incluir:
    - Descrição da tarefa do agente
    - Comportamento esperado
    - Limitações e restrições
    - Exemplos de entrada e saída
    - Instruções específicas sobre o processamento
    
    Retorne apenas o conteúdo do prompt, sem explicações adicionais.
    """
    
    if agent_prompt:
        prompt += f"\n\nInstruções adicionais: {agent_prompt}"
    
    try:
        return generate_with_openai(PROMPT_SYSTEM_MESSAGE, prompt, 1000)
    except Exception as e:
        raise Exception(f"Erro ao gerar arquivo de prompt: {str(e)}")

@router.post("/execute", response_model=OutputModel)
async def execute(input_data: InputModel):
    """
    Endpoint principal para execução do agente.
    Gera os arquivos necessários para implementar a funcionalidade de um agente.
    """
    try:
        logger.info(f"Iniciando geração de funcionalidades para o agente {input_data.agent_name}")
        
        # Validar schemas
        validate_schema(input_data.input_schema)
        validate_schema(input_data.output_schema)
        
        generated_files = []
        
        # Gerar controller
        controller_content = generate_controller(
            input_data.agent_name, 
            input_data.agent_description, 
            input_data.input_schema, 
            input_data.output_schema,
            input_data.agent_prompt
        )
        generated_files.append(GeneratedFile(
            filename="app/controllers/agent_controller.py",
            content=controller_content
        ))
        
        # Gerar testes
        tests_content = generate_tests(
            input_data.agent_name,
            input_data.agent_description,
            input_data.input_schema,
            input_data.output_schema
        )
        generated_files.append(GeneratedFile(
            filename="tests/test_main.py",
            content=tests_content
        ))
        
        # Gerar README
        readme_content = generate_readme(
            input_data.agent_name,
            input_data.agent_description,
            input_data.input_schema,
            input_data.output_schema
        )
        generated_files.append(GeneratedFile(
            filename="README.md",
            content=readme_content
        ))
        
        # Gerar arquivo de prompt
        prompt_content = generate_prompt_file(
            input_data.agent_name,
            input_data.agent_description,
            input_data.input_schema,
            input_data.output_schema,
            input_data.agent_prompt
        )
        generated_files.append(GeneratedFile(
            filename="agent_prompt.txt",
            content=prompt_content
        ))
        
        logger.info(f"Geração de funcionalidades concluída com sucesso para o agente {input_data.agent_name}")
        return OutputModel(files=generated_files)
        
    except ValueError as e:
        logger.error(f"Erro de validação: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erro interno: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """
    Endpoint para verificar a saúde do serviço.
    """
    return {"status": "healthy"} 