import requests
import logging
from datetime import datetime, timedelta


class IPCAService:
    # URL da API do Banco Central
    API_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json"
    
    # Cache para armazenar o valor do IPCA e evitar chamadas repetidas
    _cache = {
        'valor': None,
        'timestamp': None,
        'validade': timedelta(hours=24)  # Cache válido por 24 horas
    }
    
    @classmethod
    def obter_ipca_mensal(cls):
        # Verifica se há valor em cache válido
        agora = datetime.now()
        if cls._cache['valor'] is not None and cls._cache['timestamp'] is not None:
            if agora - cls._cache['timestamp'] < cls._cache['validade']:
                return cls._cache['valor']
        
        try:
            resposta = requests.get(cls.API_URL, timeout=10)  # Adiciona timeout na requisição
            resposta.raise_for_status()  # Levanta exceção para erros HTTP
            dados = resposta.json()
            
            if not dados or 'valor' not in dados[0]:
                raise ValueError("Dados do IPCA não encontrados na resposta da API")
            
            # Atualiza o cache
            cls._cache['valor'] = float(dados[0]['valor'])
            cls._cache['timestamp'] = agora
            
            return cls._cache['valor']
            
        except requests.RequestException as e:
            logging.error(f"Erro na requisição à API do Banco Central: {str(e)}")
            print(f"Erro ao conectar com a API do Banco Central: {str(e)}")
            print("Usando valor padrão de 0.5% para o IPCA")
            return 0.5  # Valor padrão caso a API falhe
            
        except (ValueError, KeyError, IndexError) as e:
            logging.error(f"Erro ao processar resposta da API: {str(e)}")
            print(f"Erro ao processar dados de IPCA: {str(e)}")
            print("Usando valor padrão de 0.5% para o IPCA")
            return 0.5  # Valor padrão caso haja erro no processamento