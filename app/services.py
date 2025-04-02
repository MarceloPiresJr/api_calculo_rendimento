from calculations.rendimento_calculator import RendimentoCalculator
from .models import RendimentoRequest, RendimentoResponse, InformeDeRendimento
from datetime import datetime
import locale
from typing import List, Tuple
from services.cdi_service import CDIService

# Configuração de localização para formatação de datas em português
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR')
    except locale.Error:
        pass


class RendimentoService:
    """
    Serviço responsável por gerenciar cálculos de rendimento financeiro.
    Atua como intermediário entre a API e o cálculo financeiro em si.
    """

    @staticmethod
    def calcular_rendimento(request: RendimentoRequest) -> RendimentoResponse:
        """
        Orquestra o processo de cálculo de rendimento baseado em uma requisição.
        
        Args:
            request: Dados da requisição com parâmetros de cálculo
            
        Returns:
            Objeto de resposta contendo o resultado detalhado do cálculo
            
        Raises:
            ValueError: Se algum parâmetro da requisição for inválido
        """
        RendimentoService._validar_dados_entrada(request)
        
        # Complementa a taxa CDI se não fornecida
        RendimentoService._complementar_taxa_cdi(request)
        
        # Calcula os rendimentos
        calculadora = RendimentoService._criar_calculadora(request)
        resultado, total_rendimento = calculadora.calcular()
        
        # Processa resultado para resposta formatada
        informe_mensal = RendimentoService._criar_informe_de_rendimento(resultado)
        valor_total_aplicado = RendimentoService._calcular_valor_total_aplicado(request)
        
        # Monta a resposta
        return RendimentoResponse(
            informe_de_rendimento=informe_mensal,
            total_rendimento=round(total_rendimento, 2),
            valor_total_aplicado=round(valor_total_aplicado, 2),
            taxa_cdi_utilizada=request.taxa_cdi_anual
        )

    @staticmethod
    def _validar_dados_entrada(request: RendimentoRequest) -> None:
        """
        Valida se os dados de entrada são consistentes.
        
        Args:
            request: Objeto de requisição com dados a validar
            
        Raises:
            ValueError: Se algum parâmetro for inválido
        """
        if request.valor_inicial < 0:
            raise ValueError("O valor inicial não pode ser negativo.")
        if request.aporte_mensal < 0:
            raise ValueError("O aporte mensal não pode ser negativo.")
        if request.mes_final < 1 or request.mes_final > 12:
            raise ValueError("O mês deve estar entre 1 e 12.")
        if request.taxa_cdi_anual is not None and request.taxa_cdi_anual < 0:
            raise ValueError("A taxa de CDI não pode ser negativa.")

    @staticmethod
    def _complementar_taxa_cdi(request: RendimentoRequest) -> None:
        """
        Obtém e preenche a taxa de CDI da API se não fornecida na requisição.
        
        Args:
            request: Objeto de requisição a ser complementado
        """
        if request.taxa_cdi_anual is None:
            request.taxa_cdi_anual = CDIService.obter_cdi_anual()

    @staticmethod
    def _criar_calculadora(request: RendimentoRequest) -> RendimentoCalculator:
        """
        Cria uma instância da calculadora de rendimentos com os parâmetros da requisição.
        
        Args:
            request: Dados de requisição com parâmetros do cálculo
            
        Returns:
            Calculadora inicializada com os parâmetros da requisição
        """
        return RendimentoCalculator(
            valor_inicial=request.valor_inicial,
            aporte_mensal=request.aporte_mensal,
            ano_final=request.ano_final,
            mes_final=request.mes_final,
            taxa_cdi_anual=request.taxa_cdi_anual
        )

    @staticmethod
    def _calcular_valor_total_aplicado(request: RendimentoRequest) -> float:
        """
        Calcula o valor total aplicado (inicial + aportes) sem rendimentos.
        
        Args:
            request: Dados da requisição
            
        Returns:
            Valor total aplicado
        """
        data_atual = datetime.today()
        numero_meses = ((request.ano_final - data_atual.year) * 12) + request.mes_final - data_atual.month
        
        return request.valor_inicial + (request.aporte_mensal * numero_meses)

    @staticmethod
    def _criar_informe_de_rendimento(
        resultado: List[Tuple[str, float, float]]
    ) -> List[InformeDeRendimento]:
        """
        Converte o resultado bruto do cálculo para um formato estruturado de resposta.
        
        Args:
            resultado: Lista de tuplas (mes_ano, saldo, rendimento)
            
        Returns:
            Lista de objetos InformeDeRendimento formatados
        """
        informe_de_rendimento = []
        
        for mes_ano, saldo, rendimento in resultado:
            mes, ano = map(int, mes_ano.split('/'))
            
            # Formata o mês por extenso em português
            data = datetime(ano, mes, 1)
            mes_formatado = data.strftime("%B") + f"/{ano}"
            
            informe_de_rendimento.append(
                InformeDeRendimento(
                    mes_ano=mes_formatado,
                    valor_total=round(saldo, 2),
                    rendimento_mensal=round(rendimento, 2)
                )
            )
            
        return informe_de_rendimento