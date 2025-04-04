from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

# Modelo de entrada para o agente
class InputModel(BaseModel):
    agent_name: str = Field(..., description="Nome do agente a ser gerado")
    agent_description: str = Field(..., description="Descrição do agente a ser gerado")
    input_schema: Dict[str, Any] = Field(..., description="Schema de entrada do agente")
    output_schema: Dict[str, Any] = Field(..., description="Schema de saída do agente")
    agent_prompt: Optional[str] = Field(None, description="Prompt adicional com instruções específicas")

# Modelo para representar um arquivo gerado
class GeneratedFile(BaseModel):
    path: str = Field(..., description="Caminho do arquivo")
    content: str = Field(..., description="Conteúdo do arquivo")

# Modelo de saída para o agente
class OutputModel(BaseModel):
    files: List[GeneratedFile] = Field(..., description="Lista de arquivos gerados")
    status: str = Field(..., description="Status da operação (success/error)")
    message: str = Field(..., description="Mensagem informativa sobre a operação") 