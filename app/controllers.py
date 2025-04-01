from fastapi import FastAPI, HTTPException
from .models import RendimentoRequest, RendimentoResponse
from .services import RendimentoService

app = FastAPI()

@app.post("/calcular_rendimento", response_model=RendimentoResponse)
async def calcular_rendimento(request: RendimentoRequest):
    try:
        return RendimentoService.calcular_rendimento(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 