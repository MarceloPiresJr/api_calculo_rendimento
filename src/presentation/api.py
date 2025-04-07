from fastapi import FastAPI
from src.interfaces.api.controllers import router as api_router


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
    
    # Adiciona as rotas da API
    app.include_router(api_router, prefix="/api/v1")
    
    # Aqui poderiam ser adicionados middlewares, eventos, etc.
    
    return app


# Instância da aplicação para ser usada pelo servidor ASGI
app = create_api() 