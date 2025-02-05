# Use a imagem oficial do Python como base
FROM python:3.9-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o arquivo de dependências (requirements.txt) para o container
COPY requirements.txt /app/requirements.txt

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código fonte para o container
COPY . /app

# Comando para rodar o script
CMD ["python", "main.py"]
