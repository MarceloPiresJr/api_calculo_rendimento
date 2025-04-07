# API de Cálculo de Rendimento

API para cálculo de rendimentos financeiros baseados na taxa CDI, implementada com Clean Architecture.

## Estrutura do Projeto

O projeto segue os princípios de Clean Architecture e Clean Code:

```
src/
├── application/             # Casos de uso da aplicação
├── domain/                  # Regras de negócio e entidades
│   ├── entities/            # Entidades de domínio
│   ├── services/            # Serviços de domínio
│   └── value_objects/       # Objetos de valor
├── infrastructure/          # Implementações concretas
│   └── external/            # Serviços externos (BCB, etc)
├── interfaces/              # Adaptadores de interface
│   ├── api/                 # Interface da API
│   │   └── dtos/            # DTOs da API
│   └── converters/          # Conversores entre domínio e DTOs
└── presentation/            # Camada de apresentação (FastAPI)

docker/                      # Arquivos para containerização (cópias de backup)
tests/                       # Testes automatizados
├── unit/                    # Testes unitários
└── integration/             # Testes de integração
web/                         # Interface frontend para a API
├── assets/                  # Recursos estáticos (JS, CSS, imagens)
└── index.html               # Página principal do site

Dockerfile                   # Arquivo de configuração do Docker
docker-compose.yml           # Arquivo de configuração do Docker Compose
```

### Camadas e Responsabilidades

1. **Domain**: Contém as regras de negócio e entidades, independente de frameworks.
2. **Application**: Contém os casos de uso da aplicação, orquestrando as entidades.
3. **Infrastructure**: Implementações concretas de serviços externos.
4. **Interfaces**: Adaptadores para comunicação entre camadas.
5. **Presentation**: Configura a API e expõe os endpoints.
6. **Web**: Interface de usuário para consumir a API.

## Funcionalidades

- Cálculo de rendimento de investimento baseado em CDI
- Cálculo de juros de saque antecipado
- Consulta da taxa CDI atual do Banco Central
- Interface web para visualização e cálculo de rendimentos

## Requisitos

- Python 3.8+
- FastAPI
- Uvicorn
- Pydantic
- Requests

## Como Executar

### API (Backend)

#### Localmente

1. Clone o repositório
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Execute a aplicação:
   ```
   python main.py
   ```
   
#### Com Docker

```
docker-compose up
```

### Site (Frontend)

1. Certifique-se que a API está em execução (porta 8000)
2. Navegue até o diretório `web`:
   ```
   cd web
   ```
3. Inicie um servidor web simples:
   ```
   # Com Python 3
   python -m http.server 8080
   ```
4. Acesse o site em: http://localhost:8080

Para instruções mais detalhadas, consulte o [README do site](web/README.md).

## Endpoints da API

### Calcular Rendimento
`POST /api/v1/calcular_rendimento`

### Calcular Juros de Saque
`POST /api/v1/calcular_juros_saque`

### Obter CDI Atual
`GET /api/v1/cdi_atual`

### Health Check
`GET /api/v1/health`

## Acesso à Documentação

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 