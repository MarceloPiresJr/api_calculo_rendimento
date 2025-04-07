import uvicorn
import os
from dotenv import load_dotenv
from src.presentation.api import app
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# Carregar variáveis de ambiente do arquivo .env (se existir)
load_dotenv()

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
    
    # Aqui poderiam ser adicionados middlewares, eventos, etc.
    
    return app

# Instância da aplicação para ser usada pelo servidor ASGI
if app_type == "static":
    from static_server import app as static_app
    app = static_app  # Aplicativo para servir o site
else:
    app = create_api()

# Monta os arquivos estáticos da pasta web/assets
app.mount("/assets", StaticFiles(directory="web/assets"), name="assets")

# Rota para a página inicial e qualquer outra rota (SPA)
@app.get("/{full_path:path}")
async def serve_site(full_path: str = ""):
    # Se for a raiz ou um caminho que não existe, retorne o index.html
    if full_path == "" or not os.path.exists(f"web/{full_path}"):
        return FileResponse("web/index.html")
    # Caso contrário, retorne o arquivo solicitado
    return FileResponse(f"web/{full_path}")

if __name__ == "__main__":
    # Obter a porta da variável de ambiente (para Render) ou usar 8000 como padrão
    port = int(os.environ.get("PORT", 8000))
    
    # Obter o host da variável de ambiente ou usar 0.0.0.0 como padrão
    host = os.environ.get("HOST", "0.0.0.0")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True
    ) 