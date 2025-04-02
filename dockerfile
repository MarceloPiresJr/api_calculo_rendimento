# Usar uma imagem base do Python
FROM python:3.9-slim

# Instalar dependências e o Heroku CLI
RUN apt-get update && \
    apt-get install -y curl && \
# Instalar locales e configurar o locale
RUN apt-get install -y locales && \
    echo "pt_BR.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen pt_BR.UTF-8 && \
    update-locale LANG=pt_BR.UTF-8

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de requisitos e instalar as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação
COPY . .

# Expor a porta que a aplicação usará
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "app.main:api_app", "--host", "0.0.0.0", "--port", "8000"]