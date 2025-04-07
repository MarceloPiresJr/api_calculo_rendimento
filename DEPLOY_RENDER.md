# Implantação no Render

Este guia explica como implantar a aplicação (API e site) na plataforma Render.

## Opções de Implantação

Existem duas maneiras de implantar este projeto no Render:

### 1. Usando o Blueprint (recomendado)

O arquivo `render.yaml` é um Blueprint que configura automaticamente ambos os serviços (API e site) juntos.

1. Faça fork deste repositório para sua conta do GitHub
2. No dashboard do Render, clique em "New" e selecione "Blueprint"
3. Conecte sua conta GitHub e selecione o repositório
4. O Render detectará automaticamente o arquivo `render.yaml` e configurará os serviços

### 2. Implantação manual

Você pode criar manualmente cada serviço:

#### API (Backend)

1. No dashboard do Render, clique em "New" e selecione "Web Service"
2. Conecte seu repositório GitHub
3. Configure:
   - **Nome**: api-calculo-rendimento
   - **Ambiente**: Python
   - **Comando de Build**: `pip install -r requirements.txt`
   - **Comando de Start**: `python main.py`
   - **Variáveis de Ambiente**:
     - `PYTHON_VERSION`: 3.10.12
     - `PORT`: 8000
     - `HOST`: 0.0.0.0
   - **Caminho de Health Check**: `/api/v1/health`

#### Site (Frontend)

1. No dashboard do Render, clique em "New" e selecione "Static Site"
2. Conecte seu repositório GitHub
3. Configure:
   - **Nome**: site-calculo-rendimento
   - **Diretório de Publicação**: `web`
   - **Comando de Build**: (deixe em branco)

## Após a Implantação

1. Após a implantação bem-sucedida dos dois serviços, anote a URL do serviço da API
2. Atualize o arquivo `web/assets/js/script.js` substituindo a URL `https://api-calculo-rendimento.onrender.com/api/v1` pela URL real da sua API
3. Faça commit e push dessas alterações
4. O site estático será automaticamente reimplantado

## Observações Importantes

- O plano gratuito do Render tem limitações de recursos e pode desativar serviços após períodos de inatividade
- O primeiro carregamento após inatividade pode ser lento (30-60 segundos)
- CORS já está configurado na API para permitir requisições de qualquer origem 