import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional


class CDIService:
    """
    Serviço responsável por consultar a taxa CDI atualizada do Banco Central do Brasil.
    Implementa um mecanismo de cache para evitar chamadas desnecessárias à API.
    """
    
    # Constantes
    BCB_API_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados/ultimos/30?formato=json"
    TEMPO_VALIDADE_CACHE = timedelta(hours=24)
    VALOR_CDI_PADRAO = 13.25  # Valor de fallback
    
    # Estrutura de cache
    _cache: Dict[str, Any] = {
        'valor': None,
        'timestamp': None,
    }
    
    @classmethod
    def obter_cdi_anual(cls) -> float:
        """
        Obtém o valor anualizado do CDI baseado nos últimos dados disponíveis.
        
        Returns:
            float: Valor anual do CDI em percentual (ex: 13.25 para 13.25%)
        """
        valor_em_cache = cls._obter_valor_do_cache()
        
        if valor_em_cache is not None:
            return valor_em_cache
            
        try:
            return cls._consultar_api_bcb()
        except Exception as erro:
            return cls._tratar_erro_api(erro)
    
    @classmethod
    def _obter_valor_do_cache(cls) -> Optional[float]:
        """
        Verifica e retorna o valor em cache se ele ainda for válido.
        
        Returns:
            Optional[float]: Valor do CDI em cache ou None se inválido/expirado
        """
        agora = datetime.now()
        
        if (cls._cache['valor'] is not None and 
            cls._cache['timestamp'] is not None and 
            agora - cls._cache['timestamp'] < cls.TEMPO_VALIDADE_CACHE):
            return cls._cache['valor']
            
        return None
    
    @classmethod
    def _consultar_api_bcb(cls) -> float:
        """
        Consulta a API do Banco Central para obter o valor atualizado do CDI.
        
        Returns:
            float: Valor anual do CDI em percentual
            
        Raises:
            requests.RequestException: Erro na comunicação com a API
            ValueError: Erro no formato ou ausência de dados na resposta
        """
        resposta = cls._fazer_requisicao_api()
        return cls._processar_resposta_api(resposta)
    
    @classmethod
    def _fazer_requisicao_api(cls) -> Dict:
        """Executa a requisição HTTP para a API do Banco Central"""
        resposta = requests.get(cls.BCB_API_URL, timeout=10)
        resposta.raise_for_status()
        return resposta.json()
    
    @classmethod
    def _processar_resposta_api(cls, dados: Dict) -> float:
        """
        Processa os dados da resposta da API, convertendo a taxa diária para anual.
        
        Args:
            dados: Resposta JSON da API
            
        Returns:
            float: Taxa anual calculada do CDI
        """
        if not dados or 'valor' not in dados[-1]:
            raise ValueError("Dados do CDI não encontrados na resposta da API")
        
        # Converte taxa diária para anual (252 dias úteis)
        taxa_diaria = float(dados[-1]['valor'])
        taxa_anual = ((1 + taxa_diaria/100) ** 252 - 1) * 100
        
        # Atualiza o cache
        cls._atualizar_cache(round(taxa_anual, 2))
        
        return cls._cache['valor']
    
    @classmethod
    def _atualizar_cache(cls, valor: float) -> None:
        """Atualiza o cache com o novo valor e timestamp"""
        cls._cache['valor'] = valor
        cls._cache['timestamp'] = datetime.now()
    
    @classmethod
    def _tratar_erro_api(cls, erro: Exception) -> float:
        """
        Trata erros ocorridos durante a consulta à API.
        Registra o erro no log e retorna um valor padrão.
        
        Args:
            erro: Exceção ocorrida
            
        Returns:
            float: Valor padrão do CDI
        """
        if isinstance(erro, requests.RequestException):
            logging.error(f"Erro na requisição à API do Banco Central: {str(erro)}")
            print(f"Erro ao conectar com a API do Banco Central: {str(erro)}")
        else:
            logging.error(f"Erro ao processar resposta da API: {str(erro)}")
            print(f"Erro ao processar dados de CDI: {str(erro)}")
            
        print(f"Usando valor padrão de {cls.VALOR_CDI_PADRAO}% para o CDI anual")
        return cls.VALOR_CDI_PADRAO 