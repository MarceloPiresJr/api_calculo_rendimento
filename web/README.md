# Site para Calculadora de Rendimentos

Este site é uma interface de usuário para a API de Cálculo de Rendimentos Financeiros.

## Funcionalidades

- Cálculo de rendimentos financeiros com base em taxa CDI
- Cálculo de juros de saque em investimentos
- Obtenção da taxa CDI atual via API
- Visualização de resultados em tabela detalhada
- Exportação de resultados para CSV

## Requisitos

- API de Cálculo de Rendimentos em execução (porta 8000)
- Servidor web simples para servir os arquivos estáticos

## Como executar

### 1. Certifique-se que a API está em execução

A API deve estar rodando na porta 8000. Caso esteja rodando em outra porta ou endereço, atualize a constante `API_BASE_URL` no arquivo `assets/js/script.js`.

Para iniciar a API:

```bash
cd ..
python main.py
```

### 2. Inicie um servidor web para os arquivos estáticos

Você pode usar qualquer servidor web de sua preferência para servir os arquivos estáticos. Alguns exemplos:

#### Usando Python:

```bash
# Python 3
python -m http.server 8080

# OU para Python 2
python -m SimpleHTTPServer 8080
```

#### Usando Node.js:

Se você tem o Node.js instalado, pode usar o pacote `serve`:

```bash
# Instalar globalmente (se ainda não tiver)
npm install -g serve

# Iniciar o servidor
serve -s . -p 8080
```

### 3. Acesse o site

Abra seu navegador e acesse: http://localhost:8080

## Observações importantes

- O site se comunica com a API via chamadas HTTP
- CORS está configurado na API para permitir essas chamadas
- Tanto a API quanto o site devem estar em execução para o funcionamento completo

## Tecnologias utilizadas

- HTML5
- CSS3 com Bootstrap 5
- JavaScript puro (sem frameworks)

## Estrutura de arquivos

```
web/
├── assets/
│   ├── css/
│   │   └── styles.css       # Estilos específicos do site
│   ├── js/
│   │   └── script.js        # Lógica JavaScript para interação com a API
│   └── img/                 # Pasta para imagens (se necessário)
├── index.html               # Página principal do site
└── README.md                # Este arquivo
```

## Próximos passos

- Implementar mais opções de cálculo
- Adicionar visualização em gráficos
- Permitir comparação entre diferentes cenários de investimento 