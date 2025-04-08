from datetime import datetime
from typing import List, Tuple, Optional


class CalculadoraRendimento:
    """
    Classe responsável pelo cálculo de rendimentos com base no CDI.
    
    Esta classe implementa a lógica principal de cálculos financeiros.
    Segue o princípio de responsabilidade única, focando apenas na lógica de cálculo.
    """
    
    def __init__(self, valor_inicial: float, aporte_mensal: float, 
                 ano_final: int, mes_final: int, taxa_cdi_anual: float, 
                 data_inicial: Optional[datetime] = None):
        """
        Inicializa a calculadora de rendimentos.
        
        Args:
            valor_inicial: Valor inicial do investimento
            aporte_mensal: Valor a ser aportado mensalmente
            ano_final: Ano final para o cálculo
            mes_final: Mês final para o cálculo (1-12)
            taxa_cdi_anual: Taxa de CDI anual em percentual
            data_inicial: Data inicial do cálculo. Se None, usa a data atual.
        """
        self.valor_inicial = valor_inicial
        self.aporte_mensal = aporte_mensal
        self.data_final = datetime(ano_final, mes_final, 1)
        self.taxa_cdi_mensal = taxa_cdi_anual / 100 / 12  # Converte a taxa anual para mensal
        self.data_inicial = data_inicial or datetime.today()
        
        self.saldo = 0.0
        self.total_rendimento = 0.0
        self.historico = []
    
    def calcular(self) -> Tuple[List[Tuple[str, float, float]], float]:
        """
        Calcula os rendimentos mês a mês até a data final.
        
        Returns:
            Tupla contendo:
                - Lista de tuplas (mês/ano, saldo, rendimento mensal)
                - Valor total de rendimentos no período
        """
        self._inicializar_calculo()
        self._validar_datas()
        
        data_atual = self.data_inicial
        
        while data_atual <= self.data_final:
            self._processar_mes(data_atual)
            data_atual = self._avancar_para_proximo_mes(data_atual)
        
        return self.historico, self.total_rendimento
    
    def _inicializar_calculo(self) -> None:
        """Reinicia os valores para um novo cálculo"""
        self.saldo = self.valor_inicial
        self.total_rendimento = 0.0
        self.historico = []
    
    def _validar_datas(self) -> None:
        """Valida se as datas de início e fim são coerentes"""
        if self.data_final <= self.data_inicial:
            raise ValueError("A data final deve ser posterior à data inicial")
    
    def _processar_mes(self, data_atual: datetime) -> None:
        """Processa o cálculo de rendimento para um mês específico"""
        self._aplicar_aporte_mensal(data_atual)
        self._aplicar_rendimento_mensal()
        self._registrar_no_historico(data_atual)
    
    def _aplicar_aporte_mensal(self, data_atual: datetime) -> None:
        """Aplica o aporte mensal ao saldo, exceto no primeiro mês com valor inicial"""
        eh_primeiro_mes = (data_atual.month == self.data_inicial.month and 
                           data_atual.year == self.data_inicial.year)
        
        if not (eh_primeiro_mes and self.valor_inicial > 0):
            self.saldo += self.aporte_mensal
    
    def _aplicar_rendimento_mensal(self) -> None:
        """Calcula e aplica o rendimento mensal ao saldo"""
        rendimento = self.saldo * self.taxa_cdi_mensal
        self.saldo += rendimento
        self.total_rendimento += rendimento
    
    def _registrar_no_historico(self, data_atual: datetime) -> None:
        """Registra o saldo e rendimento do mês atual no histórico"""
        self.historico.append((
            data_atual.strftime('%m/%Y'),
            round(self.saldo, 2),
            round(self.saldo * self.taxa_cdi_mensal, 2)
        ))
    
    def _avancar_para_proximo_mes(self, data_atual: datetime) -> datetime:
        """Retorna a data do próximo mês"""
        mes = data_atual.month + 1
        ano = data_atual.year
        
        if mes > 12:
            mes = 1
            ano += 1
            
        return datetime(ano, mes, 1)
    
    def calcular_impostos_resgate(self, considerar_ir: bool = True, considerar_iof: bool = True) -> Tuple[List[Tuple[str, float, float, float]], float]:
        """
        Calcula os impostos que seriam pagos para resgatar o dinheiro a cada mês.
        
        Args:
            considerar_ir: Se deve considerar Imposto de Renda no cálculo
            considerar_iof: Se deve considerar IOF para resgates em menos de 30 dias
            
        Returns:
            Tupla contendo:
                - Lista de tuplas (mês/ano, saldo, imposto total, alíquota IR)
                - Valor total de impostos no período
        """
        # Reset os valores para um novo cálculo
        self.saldo = self.valor_inicial
        
        # Valida as datas
        self._validar_datas()
        
        data_atual = self.data_inicial
        
        # Lista para armazenar os resultados de impostos de resgate
        historico_impostos = []
        
        # Total de impostos que seriam pagos no período
        total_impostos = 0.0
        
        # Controle dos dias decorridos para cálculo das alíquotas de IR e IOF
        dias_decorridos = 0
        
        while data_atual <= self.data_final:
            # Aplica o rendimento mensal
            rendimento = self.saldo * self.taxa_cdi_mensal
            self.saldo += rendimento
            
            # Arredonda o saldo para 2 casas decimais
            self.saldo = round(self.saldo, 2)
            
            # Calcula os dias decorridos para determinação de alíquotas
            dias_decorridos += 30  # Aproximação - mês comercial de 30 dias
            
            # Calcula o lucro sobre o qual incide IR (rendimento)
            lucro = rendimento
            
            # Calcula a alíquota de IR com base no prazo
            aliquota_ir = self._calcular_aliquota_ir(dias_decorridos) if considerar_ir else 0
            
            # Calcula o valor do IR
            imposto_renda = lucro * (aliquota_ir / 100) if considerar_ir else 0
            
            # Calcula o IOF (apenas para resgates até 30 dias)
            iof = self._calcular_iof(dias_decorridos, lucro) if considerar_iof else 0
            
            # Imposto total
            imposto_total = imposto_renda + iof
            imposto_total = round(imposto_total, 2)
            total_impostos += imposto_total
            
            # Armazena os dados do mês
            mes_ano = data_atual.strftime('%m/%Y')
            historico_impostos.append((
                mes_ano,
                self.saldo,
                imposto_total,
                aliquota_ir
            ))
            
            # Avança para o próximo mês
            data_atual = self._avancar_para_proximo_mes(data_atual)
            
            # Adiciona o aporte mensal para o próximo mês, usando a mesma lógica do método calcular
            if data_atual <= self.data_final:
                eh_primeiro_mes = (data_atual.month == self.data_inicial.month and 
                               data_atual.year == self.data_inicial.year)
                
                if not (eh_primeiro_mes and self.valor_inicial > 0):
                    self.saldo += self.aporte_mensal
        
        # Arredonda o total de impostos para 2 casas decimais
        total_impostos = round(total_impostos, 2)
        
        return historico_impostos, total_impostos
    
    def _calcular_aliquota_ir(self, dias_decorridos: int) -> float:
        """
        Calcula a alíquota de IR com base no tempo do investimento.
        
        Args:
            dias_decorridos: Dias decorridos desde o início do investimento
            
        Returns:
            Alíquota de IR em percentual
        """
        # Alíquotas regressivas de IR para investimentos em Renda Fixa (em %)
        if dias_decorridos <= 180:  # Até 180 dias
            return 22.5
        elif dias_decorridos <= 360:  # De 181 a 360 dias
            return 20.0
        elif dias_decorridos <= 720:  # De 361 a 720 dias
            return 17.5
        else:  # Acima de 720 dias
            return 15.0
    
    def _calcular_iof(self, dias_decorridos: int, rendimento: float) -> float:
        """
        Calcula o IOF com base no tempo do investimento e no rendimento.
        IOF é cobrado apenas nos primeiros 30 dias, com alíquotas regressivas.
        
        Args:
            dias_decorridos: Dias decorridos desde o início do investimento
            rendimento: Rendimento sobre o qual incide o IOF
            
        Returns:
            Valor do IOF
        """
        # IOF só é cobrado nos primeiros 30 dias
        if dias_decorridos > 30:
            return 0.0
        
        # Tabela regressiva de IOF
        aliquotas_iof = [
            96, 93, 90, 86, 83, 80, 76, 73, 70, 66, 63, 60, 56, 53, 50, 46, 
            43, 40, 36, 33, 30, 26, 23, 20, 16, 13, 10, 6, 3, 0
        ]
        
        # A posição no array é o dia - 1 (pois o array começa em 0)
        # Limitamos a 29 para evitar acesso fora do array
        dia_indice = min(dias_decorridos - 1, 29)
        aliquota = aliquotas_iof[dia_indice] / 100
        
        return rendimento * aliquota
    
    def obter_saldo_final(self) -> float:
        """Retorna o saldo final após o cálculo."""
        if not self.historico:
            return self.valor_inicial
        return self.historico[-1][1] 