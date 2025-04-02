from pydantic import BaseModel
from typing import List, Tuple, Dict

class RendimentoRequest(BaseModel):
    valor_inicial: float
    aporte_mensal: float
    ano_final: int
    mes_final: int
    taxa_cdi_anual: float

class InformeDeRendimento(BaseModel):
    mes_ano: str
    valor_total: float
    rendimento_mensal: float

class RendimentoResponse(BaseModel):
    informe_de_rendimento: List[InformeDeRendimento]
    total_rendimento: float
    valor_total_aplicado: float 