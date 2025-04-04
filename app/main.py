from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.agent_controller import router as agent_router
import os
import time
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Criar a aplicação FastAPI
app = FastAPI(
    title="generate-agent-functionality-agent",
    description="Um agente especializado em gerar funcionalidades para outros agentes utilizando IA",
    version="0.1.0",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique as origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para logging de requisições
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(
        f"Method: {request.method} Path: {request.url.path} "
        f"Status: {response.status_code} Time: {process_time:.2f}s"
    )
    return response

# Incluir routers
app.include_router(agent_router)

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Endpoint para verificação de saúde da API.
    """
    return {"status": "healthy"} 