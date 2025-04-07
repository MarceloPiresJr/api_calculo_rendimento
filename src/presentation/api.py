from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.interfaces.api.controllers import router as api_router
import os

# Obter o tipo de app da variável de ambiente
app_type = os.environ.get("APP_TYPE", "api")

def create_api() -> FastAPI:
    """
    Cria e configura a aplicação FastAPI.
    
    Returns:
        FastAPI: Aplicação configurada com rotas e middlewares
    """
    # Cria a aplicação FastAPI com configurações
    app = FastAPI(
        title="API de Cálculo de Rendimentos",
        description="API para cálculo de rendimentos financeiros com base em CDI",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    # Configuração de CORS para permitir requisições do frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://web-calculo-rendimento.onrender.com",  # URL específica do seu site
            "http://localhost:8080",  # Para desenvolvimento local
            "*"  # Opcional: permite todas as origens
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Adiciona as rotas da API
    app.include_router(api_router, prefix="/api/v1")
    
    return app

# Instância da aplicação para ser usada pelo servidor ASGI
app = create_api()