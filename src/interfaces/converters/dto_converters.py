from datetime import datetime
from typing import List

from src.interfaces.api.dtos.rendimento_dtos import (
    CalculoRendimentoRequestDTO, 
    CalculoRendimentoResponseDTO,
    InformeRendimentoDTO,
    CalculoJurosSaqueRequestDTO,
    CalculoJurosSaqueResponseDTO,
    InformeJurosSaqueDTO
)
from src.interfaces.api.dtos.cdi_dtos import TaxaCDIResponseDTO

from src.domain.entities.models import (
    ParametrosCalculoRendimento,
    ParametrosCalculoJurosSaque,
    InformeRendimentoMensal,
    InformeJurosSaqueMensal,
    ResultadoCalculoRendimento,
    ResultadoCalculoJurosSaque
)


class DTOConverter:
    """
    Classe responsável por converter entre DTOs e modelos de domínio.
    Implementa o padrão Adapter para isolar a camada de API da camada de domínio.
    """
    
    @staticmethod
    def to_parametros_calculo(dto: CalculoRendimentoRequestDTO) -> ParametrosCalculoRendimento:
        """
        Converte um DTO de requisição para o modelo de parâmetros de cálculo do domínio.
        
        Args:
            dto: DTO da requisição de cálculo
            
        Returns:
            Modelo de domínio com os parâmetros de cálculo
        """
        return ParametrosCalculoRendimento(
            valor_inicial=dto.valor_inicial,
            aporte_mensal=dto.aporte_mensal,
            ano_final=dto.ano_final,
            mes_final=dto.mes_final,
            taxa_cdi_anual=dto.taxa_cdi_anual,
            percentual_sobre_cdi=dto.percentual_sobre_cdi or 100.0
        )
    
    @staticmethod
    def to_parametros_juros_saque(dto: CalculoJurosSaqueRequestDTO) -> ParametrosCalculoJurosSaque:
        """
        Converte um DTO de requisição para o modelo de parâmetros de cálculo de juros de saque.
        
        Args:
            dto: DTO da requisição de cálculo de juros
            
        Returns:
            Modelo de domínio com os parâmetros de cálculo de juros
        """
        return ParametrosCalculoJurosSaque(
            valor_inicial=dto.valor_inicial,
            aporte_mensal=dto.aporte_mensal,
            ano_final=dto.ano_final,
            mes_final=dto.mes_final,
            taxa_cdi_anual=dto.taxa_cdi_anual,
            percentual_sobre_cdi=dto.percentual_sobre_cdi or 100.0,
            taxa_juros_saque=dto.taxa_juros_saque or 1.0
        )
    
    @staticmethod
    def to_calculo_response(resultado: ResultadoCalculoRendimento) -> CalculoRendimentoResponseDTO:
        """
        Converte um resultado de cálculo do domínio para o DTO de resposta da API.
        
        Args:
            resultado: Resultado de cálculo do domínio
            
        Returns:
            DTO formatado para resposta da API
        """
        # Converte informes mensais
        informes_dto = [
            InformeRendimentoDTO(
                mes_ano=informe.mes_ano_formatado,
                valor_total=round(informe.saldo, 2),
                rendimento_mensal=round(informe.rendimento, 2)
            )
            for informe in resultado.informes_mensais
        ]
        
        # Monta o DTO de resposta
        return CalculoRendimentoResponseDTO(
            informe_mensal=informes_dto,
            total_rendimento=round(resultado.total_rendimento, 2),
            valor_total_aplicado=round(resultado.valor_total_aplicado, 2),
            taxa_cdi_utilizada=resultado.taxa_cdi_utilizada,
            percentual_sobre_cdi=resultado.percentual_sobre_cdi,
            data_calculo=resultado.data_calculo_formatada
        )
    
    @staticmethod
    def to_juros_saque_response(resultado: ResultadoCalculoJurosSaque) -> CalculoJurosSaqueResponseDTO:
        """
        Converte um resultado de cálculo de juros de saque do domínio para o DTO de resposta da API.
        
        Args:
            resultado: Resultado de cálculo de juros de saque do domínio
            
        Returns:
            DTO formatado para resposta da API
        """
        # Converte informes mensais
        informes_dto = [
            InformeJurosSaqueDTO(
                mes_ano=informe.mes_ano_formatado,
                valor_total=round(informe.saldo, 2),
                juros_saque_mensal=round(informe.juros_saque, 2)
            )
            for informe in resultado.informes_mensais
        ]
        
        # Monta o DTO de resposta
        return CalculoJurosSaqueResponseDTO(
            informe_mensal=informes_dto,
            total_juros_saque=round(resultado.total_juros_saque, 2),
            rendimento_liquido=round(resultado.rendimento_liquido, 2),
            rendimento_bruto=round(resultado.rendimento_bruto, 2),
            valor_total_aplicado=round(resultado.valor_total_aplicado, 2),
            taxa_cdi_utilizada=resultado.taxa_cdi_utilizada,
            percentual_sobre_cdi=resultado.percentual_sobre_cdi,
            taxa_juros_saque=resultado.taxa_juros_saque,
            data_calculo=resultado.data_calculo_formatada
        )
    
    @staticmethod
    def to_cdi_response(cdi_valor: float) -> TaxaCDIResponseDTO:
        """
        Cria um DTO de resposta com informações da taxa CDI.
        
        Args:
            cdi_valor: Valor da taxa CDI anual
            
        Returns:
            DTO formatado para resposta da API
        """
        return TaxaCDIResponseDTO(
            cdi_anual=cdi_valor,
            data_atualizacao=datetime.now(),
            fonte="Banco Central do Brasil"
        )
    
    @staticmethod
    def tuplas_to_informes_mensais(
        tuplas_resultado: List[tuple]
    ) -> List[InformeRendimentoMensal]:
        """
        Converte as tuplas de resultado do calculador para objetos de domínio.
        
        Args:
            tuplas_resultado: Lista de tuplas (mes_ano, saldo, rendimento)
            
        Returns:
            Lista de objetos InformeRendimentoMensal
        """
        informes = []
        
        for mes_ano, saldo, rendimento in tuplas_resultado:
            mes, ano = map(int, mes_ano.split('/'))
            data = datetime(ano, mes, 1)
            
            informe = InformeRendimentoMensal(
                data=data,
                saldo=saldo,
                rendimento=rendimento
            )
            
            informes.append(informe)
            
        return informes
    
    @staticmethod
    def tuplas_to_informes_juros_saque(
        tuplas_resultado: List[tuple]
    ) -> List[InformeJurosSaqueMensal]:
        """
        Converte as tuplas de resultado do calculador para objetos de domínio de juros de saque.
        
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