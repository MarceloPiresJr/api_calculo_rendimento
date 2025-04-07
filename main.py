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

# Cria a aplicação FastAPI
app = FastAPI(title="Calculadora de Rendimentos - Site")

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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