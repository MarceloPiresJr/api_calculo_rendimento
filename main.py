import uvicorn
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from src.presentation.api import app as api_app  # Importar o app já criado

# Carregar variáveis de ambiente
load_dotenv()

# Criar app para servir arquivos estáticos
def create_static_app():
    static_app = FastAPI(title="Calculadora de Rendimentos - Site")
    
    # Configuração de CORS
    static_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Monta os arquivos estáticos da pasta web/assets
    static_app.mount("/assets", StaticFiles(directory="web/assets"), name="assets")
    
    # Rota específica para a raiz
    @static_app.get("/")
    async def serve_root():
        return FileResponse("web/index.html")
    
    # Rota para outros caminhos
    @static_app.get("/{full_path:path}")
    async def serve_site(full_path: str):
        if os.path.exists(f"web/{full_path}"):
            return FileResponse(f"web/{full_path}")
        return FileResponse("web/index.html")
    
    return static_app

# Escolher o app com base na variável de ambiente
app_type = os.environ.get("APP_TYPE", "api")
if app_type == "static":
    app = create_static_app()
else:
    app = api_app  # Usar o app já criado em api.py

if __name__ == "__main__":
    # Obter a porta da variável de ambiente
    port = int(os.environ.get("PORT", 8000))
    
    # Obter o host da variável de ambiente
    host = os.environ.get("HOST", "0.0.0.0")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True
    ) 