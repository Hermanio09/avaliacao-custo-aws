# Use uma imagem oficial do Python como base
FROM python:3.9-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie o arquivo Python e o arquivo .env para o diretório de trabalho
COPY ec2_monitor.py /app
COPY .env /app/.env

# Instale as dependências necessárias
RUN pip install boto3 python-dotenv

# Comando para rodar o script Python quando o container iniciar
CMD ["python", "ec2_monitor.py"]
