from calculations.rendimento_calculator import RendimentoCalculator
from datetime import datetime
import locale
from typing import List, Tuple

from services.cdi_service import CDIService
from app.domain.models import (
    ParametrosCalculoRendimento,
    InformeRendimentoMensal,
    ResultadoCalculoRendimento
)
from app.domain.converters import DTOConverter

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
    Implementa a lógica de negócio para cálculo de rendimentos.
    """

    @staticmethod
    def calcular_rendimento(parametros: ParametrosCalculoRendimento) -> ResultadoCalculoRendimento:
        """
        Realiza o cálculo de rendimento usando os parâmetros de domínio.
        
        Args:
            parametros: Parâmetros para o cálculo de rendimento
            
        Returns:
            Objeto de resultado com os dados calculados
            
        Raises:
            ValueError: Se algum parâmetro for inválido
        """
        # Validação dos dados
        RendimentoService._validar_parametros(parametros)
        
        # Complementa a taxa CDI se não fornecida
        if parametros.taxa_cdi_anual is None:
            parametros.taxa_cdi_anual = CDIService.obter_cdi_anual()
        
        # Calcula os rendimentos
        calculadora = RendimentoService._criar_calculadora(parametros)
        tuplas_resultado, total_rendimento = calculadora.calcular()
        
        # Converte tuplas em objetos de domínio
        informes_mensais = DTOConverter.tuplas_to_informes_mensais(tuplas_resultado)
        
        # Calcula valor total aplicado
        valor_total_aplicado = RendimentoService._calcular_valor_total_aplicado(parametros)
        
        # Cria e retorna o resultado
        return ResultadoCalculoRendimento(
            informes_mensais=informes_mensais,
            total_rendimento=total_rendimento,
            valor_total_aplicado=valor_total_aplicado,
            taxa_cdi_utilizada=parametros.taxa_cdi_anual
        )

    @staticmethod
    def _validar_parametros(parametros: ParametrosCalculoRendimento) -> None:
        """
        Valida se os parâmetros de cálculo são consistentes.
        
        Args:
            parametros: Parâmetros a validar
            
        Raises:
            ValueError: Se algum parâmetro for inválido
        """
        if parametros.valor_inicial < 0:
            raise ValueError("O valor inicial não pode ser negativo.")
        if parametros.aporte_mensal < 0:
            raise ValueError("O aporte mensal não pode ser negativo.")
        if parametros.mes_final < 1 or parametros.mes_final > 12:
            raise ValueError("O mês deve estar entre 1 e 12.")
        if parametros.taxa_cdi_anual is not None and parametros.taxa_cdi_anual < 0:
            raise ValueError("A taxa de CDI não pode ser negativa.")
        
        data_atual = datetime.today()
        if parametros.ano_final < data_atual.year or (
                parametros.ano_final == data_atual.year and 
                parametros.mes_final < data_atual.month):
            raise ValueError("A data final deve ser posterior à data atual.")

    @staticmethod
    def _criar_calculadora(parametros: ParametrosCalculoRendimento) -> RendimentoCalculator:
        """
        Cria uma instância da calculadora de rendimentos com os parâmetros fornecidos.
        
        Args:
            parametros: Parâmetros para inicializar a calculadora
            
        Returns:
            Calculadora inicializada
        """
        return RendimentoCalculator(
            valor_inicial=parametros.valor_inicial,
            aporte_mensal=parametros.aporte_mensal,
            ano_final=parametros.ano_final,
            mes_final=parametros.mes_final,
            taxa_cdi_anual=parametros.taxa_cdi_anual,
            data_inicial=parametros.data_inicial
        )

    @staticmethod
    def _calcular_valor_total_aplicado(parametros: ParametrosCalculoRendimento) -> float:
        """
        Calcula o valor total aplicado (inicial + aportes) sem rendimentos.
        
        Args:
            parametros: Parâmetros do cálculo
            
        Returns:
            Valor total aplicado
        """
        data_atual = datetime.today() if parametros.data_inicial is None else parametros.data_inicial
        
        # Calcula número de meses entre data atual e data final
        numero_meses = ((parametros.ano_final - data_atual.year) * 12) + parametros.mes_final - data_atual.month
        
        # Garante que o número de meses não seja negativo
        numero_meses = max(0, numero_meses)
        
        return parametros.valor_inicial + (parametros.aporte_mensal * numero_meses)