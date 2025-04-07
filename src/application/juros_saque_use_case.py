from datetime import datetime
from typing import List, Tuple

from src.domain.entities.models import (
    ParametrosCalculoJurosSaque,
    ResultadoCalculoJurosSaque,
    InformeJurosSaqueMensal
)
from src.domain.services.calculadora_rendimento import CalculadoraRendimento
from src.infrastructure.external.bcb_service import CDIService


class JurosSaqueUseCase:
    """
    Caso de uso para cálculo de juros de saque.
    
    Implementa a lógica de negócio relacionada ao cálculo de juros que seriam
    pagos para sacar o dinheiro antes do prazo.
    """
    
    @staticmethod
    def calcular_juros_saque(parametros: ParametrosCalculoJurosSaque) -> ResultadoCalculoJurosSaque:
        """
        Realiza o cálculo de juros de saque usando os parâmetros de domínio.
        
        Args:
            parametros: Parâmetros para o cálculo de juros
            
        Returns:
            Objeto de resultado com os dados calculados
            
        Raises:
            ValueError: Se algum parâmetro for inválido
        """
        # Validação dos dados
        JurosSaqueUseCase._validar_parametros(parametros)
        
        # Complementa a taxa CDI se não fornecida
        if parametros.taxa_cdi_anual is None:
            parametros.taxa_cdi_anual = CDIService.obter_cdi_anual()
        
        # Calcula os rendimentos e os juros de saque
        calculadora = JurosSaqueUseCase._criar_calculadora(parametros)
        tuplas_resultado, total_juros_saque = calculadora.calcular_juros_saque(
            taxa_juros_mensal=parametros.taxa_juros_saque
        )
        
        # Converte tuplas em objetos de domínio
        informes_mensais = JurosSaqueUseCase._converter_tuplas_para_informes(tuplas_resultado)
        
        # Calcula valor total aplicado
        valor_total_aplicado = JurosSaqueUseCase._calcular_valor_total_aplicado(parametros)
        
        # Cria e retorna o resultado
        return ResultadoCalculoJurosSaque(
            informes_mensais=informes_mensais,
            total_juros_saque=total_juros_saque,
            valor_total_aplicado=valor_total_aplicado,
            taxa_cdi_utilizada=parametros.taxa_cdi_anual,
            percentual_sobre_cdi=parametros.percentual_sobre_cdi,
            taxa_juros_saque=parametros.taxa_juros_saque
        )
    
    @staticmethod
    def _validar_parametros(parametros: ParametrosCalculoJurosSaque) -> None:
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
        if parametros.percentual_sobre_cdi < 0:
            raise ValueError("O percentual sobre CDI não pode ser negativo.")
        if parametros.taxa_juros_saque < 0:
            raise ValueError("A taxa de juros de saque não pode ser negativa.")
        
        data_atual = datetime.today()
        if parametros.ano_final < data_atual.year or (
                parametros.ano_final == data_atual.year and 
                parametros.mes_final < data_atual.month):
            raise ValueError("A data final deve ser posterior à data atual.")
    
    @staticmethod
    def _criar_calculadora(parametros: ParametrosCalculoJurosSaque) -> CalculadoraRendimento:
        """
        Cria uma instância da calculadora de rendimentos com os parâmetros fornecidos.
        
        Args:
            parametros: Parâmetros para inicializar a calculadora
            
        Returns:
            Calculadora inicializada
        """
        # Calcula a taxa efetiva considerando o percentual sobre CDI
        taxa_efetiva = parametros.taxa_cdi_anual * (parametros.percentual_sobre_cdi / 100.0)
        
        return CalculadoraRendimento(
            valor_inicial=parametros.valor_inicial,
            aporte_mensal=parametros.aporte_mensal,
            ano_final=parametros.ano_final,
            mes_final=parametros.mes_final,
            taxa_cdi_anual=taxa_efetiva,
            data_inicial=parametros.data_inicial
        )
    
    @staticmethod
    def _calcular_valor_total_aplicado(parametros: ParametrosCalculoJurosSaque) -> float:
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
    
    @staticmethod
    def _converter_tuplas_para_informes(
        tuplas_resultado: List[Tuple[str, float, float]]
    ) -> List[InformeJurosSaqueMensal]:
        """
        Converte as tuplas de resultado do calculador para objetos de domínio.
        
        Args:
            tuplas_resultado: Lista de tuplas (mes_ano, saldo, juros_saque)
            
        Returns:
            Lista de objetos InformeJurosSaqueMensal
        """
        informes = []
        
        for mes_ano, saldo, juros_saque in tuplas_resultado:
            mes, ano = map(int, mes_ano.split('/'))
            data = datetime(ano, mes, 1)
            
            informe = InformeJurosSaqueMensal(
                data=data,
                saldo=saldo,
                juros_saque=juros_saque
            )
            
            informes.append(informe)
            
        return informes 