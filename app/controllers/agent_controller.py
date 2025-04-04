from fastapi import APIRouter, HTTPException, Depends
from app.models.agent_model import InputModel, OutputModel, GeneratedFile
from typing import Dict, Any, List
import os
import json
import openai
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar a API do OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

router = APIRouter(prefix="/api/v1", tags=["agent"])

def generate_controller(agent_name: str, agent_description: str, input_schema: Dict, output_schema: Dict, agent_prompt: str = None) -> str:
    """
    Gera o código do controller usando a OpenAI API.
    """
    system_message = """Você é um especialista em desenvolvimento de APIs com FastAPI. 
    Sua tarefa é gerar um arquivo controller.py para um agente conforme as especificações.
    O código deve ser bem estruturado, comentado e seguir as melhores práticas."""
    
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
        response = openai.ChatCompletion.create(
            model="gpt-4", 
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"Erro ao gerar controller: {str(e)}")

def generate_tests(agent_name: str, agent_description: str, input_schema: Dict, output_schema: Dict) -> str:
    """
    Gera o código de testes usando a OpenAI API.
    """
    system_message = """Você é um especialista em testes de API com pytest. 
    Sua tarefa é gerar um arquivo test_main.py para testar um agente conforme as especificações."""
    
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
        response = openai.ChatCompletion.create(
            model="gpt-4", 
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"Erro ao gerar testes: {str(e)}")

def generate_readme(agent_name: str, agent_description: str, input_schema: Dict, output_schema: Dict) -> str:
    """
    Gera o README.md usando a OpenAI API.
    """
    system_message = """Você é um especialista em documentação de software. 
    Sua tarefa é gerar um arquivo README.md para um agente conforme as especificações."""
    
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
        response = openai.ChatCompletion.create(
            model="gpt-4", 
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"Erro ao gerar README: {str(e)}")

def generate_prompt_file(agent_name: str, agent_description: str, input_schema: Dict, output_schema: Dict, agent_prompt: str = None) -> str:
    """
    Gera um arquivo de prompt para o agente usando a OpenAI API.
    """
    system_message = """Você é um especialista em prompts para IA. 
    Sua tarefa é gerar um arquivo de prompt detalhado para um agente conforme as especificações."""
    
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
        response = openai.ChatCompletion.create(
            model="gpt-4", 
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"Erro ao gerar arquivo de prompt: {str(e)}")

@router.post("/execute", response_model=OutputModel)
async def execute(input_data: InputModel):
    """
    Endpoint principal para execução do agente.
    Gera os arquivos necessários para implementar a funcionalidade de um agente.
    """
    try:
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
            path="app/controllers/agent_controller.py",
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
            path="tests/test_main.py",
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
            path="README.md",
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
            path="agent_prompt.txt",
            content=prompt_content
        ))
        
        return {
            "files": generated_files,
            "status": "success",
            "message": f"Geração de funcionalidades para o agente {input_data.agent_name} concluída com sucesso."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 