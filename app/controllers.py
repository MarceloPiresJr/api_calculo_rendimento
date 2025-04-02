from fastapi import FastAPI, HTTPException, Response, status
from typing import Dict, Any

from .models import RendimentoRequest, RendimentoResponse
from .services import RendimentoService
from services.cdi_service import CDIService

# Configuração da aplicação FastAPI
app = FastAPI(
    title="API de Cálculo de Rendimentos",
    description="API para cálculo de rendimentos financeiros com base em CDI",
    version="1.0.0"
)


@app.post(
    "/calcular_rendimento", 
    response_model=RendimentoResponse,
    summary="Calcula rendimentos de investimento",
    status_code=status.HTTP_200_OK
)
async def calcular_rendimento(request: RendimentoRequest) -> RendimentoResponse:
    """
    Calcula o rendimento de um investimento com base nos parâmetros fornecidos.
    
    Parameters:
    - **valor_inicial**: Valor inicial do investimento
    - **aporte_mensal**: Valor aportado mensalmente
    - **ano_final**: Ano final para o cálculo
    - **mes_final**: Mês final para o cálculo (1-12)
    - **taxa_cdi_anual**: (Opcional) Taxa de CDI anual. Se não fornecida, usa a taxa atual.
    
    Returns:
        RendimentoResponse: Detalhes do cálculo, incluindo o informe mensal e totais
    """
    try:
        return RendimentoService.calcular_rendimento(request)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )
    except Exception as e:
        # Log do erro (em um sistema de produção)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao processar a solicitação"
        )


@app.get(
    "/cdi_atual",
    summary="Obtém a taxa CDI atual",
    response_model=Dict[str, float],
    status_code=status.HTTP_200_OK
)
async def obter_cdi_atual() -> Dict[str, float]:
    """
    Retorna o valor atual da taxa CDI anual em percentual.
    
    O valor é obtido da API do Banco Central do Brasil e atualizado diariamente.
    
    Returns:
        Dict: Contendo a chave "cdi_anual" com o valor da taxa
    """
    try:
        valor_cdi = CDIService.obter_cdi_anual()
        return {"cdi_anual": valor_cdi}
    except Exception as e:
        # Em um sistema de produção, registraria o erro em log
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao consultar taxa CDI: {str(e)}"
        )


# Rotas adicionais para monitoramento e saúde da aplicação
@app.get(
    "/health",
    summary="Verifica a saúde da aplicação",
    status_code=status.HTTP_200_OK
)
async def health_check() -> Dict[str, str]:
    """
    Endpoint para verificação de saúde/disponibilidade da aplicação.
    Útil para monitoramento e health checks.
    """
    return {"status": "ok"} 