import uvicorn
from fastapi import FastAPI

# Agora o import funcionará tanto quando executado como script quanto como módulo
from app.controllers import app as api_app

if __name__ == "__main__":
    uvicorn.run(
        "app.main:api_app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )