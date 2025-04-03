# Pacote de DTOs (Data Transfer Objects)
# Contém os modelos de transferência de dados da API

# DTOs de Rendimento
from app.dtos.rendimento_dtos import (
    CalculoRendimentoRequestDTO,
    CalculoRendimentoResponseDTO,
    InformeRendimentoDTO,
    CalculoJurosSaqueRequestDTO,
    CalculoJurosSaqueResponseDTO,
    InformeJurosSaqueDTO
)

# DTOs de CDI
from app.dtos.cdi_dtos import (
    TaxaCDIResponseDTO
)

# DTOs comuns/utilitários
from app.dtos.common_dtos import (
    ErroResponseDTO,
    MensagemResponseDTO,
    PaginacaoDTO
)

# Exportação explícita de símbolos
__all__ = [
    'CalculoRendimentoRequestDTO',
    'CalculoRendimentoResponseDTO',
    'InformeRendimentoDTO',
    'CalculoJurosSaqueRequestDTO', 
    'CalculoJurosSaqueResponseDTO',
    'InformeJurosSaqueDTO',
    'TaxaCDIResponseDTO',
    'ErroResponseDTO',
    'MensagemResponseDTO',
    'PaginacaoDTO'
] 