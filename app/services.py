from calculations.rendimento_calculator import RendimentoCalculator
from .models import RendimentoRequest, RendimentoResponse, InformeDeRendimento
from datetime import datetime
import locale

# Defina o locale para português
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')  # Tente UTF-8
except locale.Error:
    locale.setlocale(locale.LC_ALL, 'pt_BR')  # Tente sem UTF-8

class RendimentoService:
    @staticmethod
    def calcular_rendimento(request: RendimentoRequest) -> RendimentoResponse:
        RendimentoService.validar_dados_entrada(request)

        calculadora = RendimentoCalculator(
            valor_inicial=request.valor_inicial,
            aporte_mensal=request.aporte_mensal,
            ano_final=request.ano_final,
            mes_final=request.mes_final,
            taxa_cdi=request.taxa_cdi
        )
        
        resultado, total_rendimento = calculadora.calcular()
        informe_de_rendimento = RendimentoService.gerar_informe_de_rendimento(resultado)

        return RendimentoResponse(
            informe_de_rendimento=informe_de_rendimento,
            total_rendimento=round(total_rendimento, 2),
            valor_total_aplicado=round(request.valor_inicial + (request.aporte_mensal * (request.ano_final - 2023) * 12), 2)
        )

    @staticmethod
    def validar_dados_entrada(request: RendimentoRequest):
        if request.valor_inicial < 0:
            raise ValueError("O valor inicial não pode ser negativo.")
        if request.aporte_mensal < 0:
            raise ValueError("O aporte mensal não pode ser negativo.")
        if request.mes_final < 1 or request.mes_final > 12:
            raise ValueError("O mês deve estar entre 1 e 12.")
        if request.taxa_cdi < 0:
            raise ValueError("A taxa de CDI não pode ser negativa.")

    @staticmethod
    def gerar_informe_de_rendimento(resultado):
        informe_de_rendimento = []
        for mes_ano, saldo, rendimento in resultado:
            mes, ano = map(int, mes_ano.split('/'))
            informe_de_rendimento.append(
                InformeDeRendimento(
                    mes_ano=datetime(ano, mes, 1).strftime("%B") + f"/{ano}",
                    valor_total=round(saldo, 2),
                    rendimento_mensal=round(rendimento, 2)
                )
            )
        return informe_de_rendimento 