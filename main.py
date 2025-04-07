import uvicorn
import os
from dotenv import load_dotenv
from src.presentation.api import app

# Carregar variáveis de ambiente do arquivo .env (se existir)
load_dotenv()

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