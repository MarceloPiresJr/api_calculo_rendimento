from fastapi import FastAPI, HTTPException, Response, status
from typing import Dict, Any

from app.dtos import (
    CalculoRendimentoRequestDTO,
    CalculoRendimentoResponseDTO,
    TaxaCDIResponseDTO
)
from app.domain.converters import DTOConverter
from app.services import RendimentoService
from services.cdi_service import CDIService

# Configuração da aplicação FastAPI
app = FastAPI(
    title="API de Cálculo de Rendimentos",
    description="API para cálculo de rendimentos financeiros com base em CDI",
    version="1.0.0"
)


@app.post(
    "/calcular_rendimento", 
    response_model=CalculoRendimentoResponseDTO,
    summary="Calcula rendimentos de investimento",
    status_code=status.HTTP_200_OK
)
async def calcular_rendimento(request_dto: CalculoRendimentoRequestDTO) -> CalculoRendimentoResponseDTO:
    """
    Calcula o rendimento de um investimento com base nos parâmetros fornecidos.
    
    Parameters:
    - **valor_inicial**: Valor inicial do investimento
    - **aporte_mensal**: Valor aportado mensalmente
    - **ano_final**: Ano final para o cálculo
    - **mes_final**: Mês final para o cálculo (1-12)
    - **taxa_cdi_anual**: (Opcional) Taxa de CDI anual. Se não fornecida, usa a taxa atual.
    
    Returns:
        CalculoRendimentoResponseDTO: Detalhes do cálculo, incluindo o informe mensal e totais
    """
    try:
        # Converte DTO para modelo de domínio
        parametros_calculo = DTOConverter.to_parametros_calculo(request_dto)
        
        # Executa o cálculo usando o serviço de domínio
        resultado = RendimentoService.calcular_rendimento(parametros_calculo)
        
        # Converte resultado do domínio para DTO de resposta
        return DTOConverter.to_calculo_response(resultado)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )
    except Exception as e:
        # Em um sistema real, registraria o erro em log
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao processar a solicitação"
        )


@app.get(
    "/cdi_atual",
    summary="Obtém a taxa CDI atual",
    response_model=TaxaCDIResponseDTO,
    status_code=status.HTTP_200_OK
)
async def obter_cdi_atual() -> TaxaCDIResponseDTO:
    """
    Retorna o valor atual da taxa CDI anual em percentual.
    
    O valor é obtido da API do Banco Central do Brasil e atualizado diariamente.
    
    Returns:
        TaxaCDIResponseDTO: Informações sobre a taxa CDI atual
    """
    try:
        valor_cdi = CDIService.obter_cdi_anual()
        return DTOConverter.to_cdi_response(valor_cdi)
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