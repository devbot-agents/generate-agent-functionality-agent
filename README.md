# Generate Agent Functionality Agent

Este agente é especializado em gerar a funcionalidade para outros agentes utilizando IA. Ele recebe informações sobre um agente (nome, descrição, schemas) e gera automaticamente:

- Controller com lógica de negócio
- Testes automáticos
- Arquivo README.md
- Arquivo de prompt 

## Instalação

```bash
pip install -r requirements.txt
```

## Executando

```bash
uvicorn app.main:app --reload
```

## Documentação da API

Após iniciar o servidor, acesse a documentação em:
http://localhost:8000/docs

## Como utilizar

Faça uma requisição POST para o endpoint `/api/v1/execute` com os seguintes dados:

```json
{
  "agent_name": "nome-do-agente",
  "agent_description": "Descrição detalhada do que o agente faz",
  "input_schema": {
    "campo1": "string",
    "campo2": "number"
  },
  "output_schema": {
    "resultado": "string",
    "status": "boolean"
  },
  "agent_prompt": "Instruções adicionais específicas para este agente (opcional)"
}
```

### Resposta

A resposta incluirá uma lista de arquivos gerados com seus respectivos caminhos e conteúdos:

```json
{
  "files": [
    {
      "path": "app/controllers/agent_controller.py",
      "content": "conteúdo do arquivo..."
    },
    {
      "path": "tests/test_main.py",
      "content": "conteúdo do arquivo..."
    },
    {
      "path": "README.md",
      "content": "conteúdo do arquivo..."
    },
    {
      "path": "agent_prompt.txt",
      "content": "conteúdo do arquivo..."
    }
  ],
  "status": "success",
  "message": "Geração de funcionalidades concluída com sucesso."
}
```

## Requisitos

- Python 3.8+
- FastAPI
- OpenAI API Key (definida como variável de ambiente OPENAI_API_KEY) 