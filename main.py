import os
import requests
import json
import schedule
import time
from datetime import datetime
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

# Carregar variáveis de ambiente
from dotenv import load_dotenv
load_dotenv()

# Configurações via variáveis de ambiente
ENV_CONFIG = {
    "URL": os.getenv("REQUEST_URL"),
    "SCHEDULE_INTERVAL_HOURS": int(os.getenv("SCHEDULE_INTERVAL_HOURS", "4")),  # Lê o intervalo de horas
    "MAX_RETRIES": int(os.getenv("MAX_RETRIES", "144")),
    "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
    "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
    "S3_BUCKET_NAME": os.getenv("S3_BUCKET_NAME")
}

def validate_env():
    required_vars = ["REQUEST_URL", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "S3_BUCKET_NAME"]
    for var in required_vars:
        if not os.getenv(var):
            raise ValueError(f"🔴 Variável de ambiente {var} não configurada!")

def upload_to_s3(filename):
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=ENV_CONFIG["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=ENV_CONFIG["AWS_SECRET_ACCESS_KEY"]
        )
        
        s3.upload_file(
            Filename=filename,
            Bucket=ENV_CONFIG["S3_BUCKET_NAME"],
            Key=filename
        )
        
        print(f"✅ Arquivo {filename} enviado para o S3 com sucesso!")
        return True

    except NoCredentialsError:
        print("🔴 Credenciais AWS não encontradas!")
        return False
    except ClientError as e:
        print(f"🔴 Erro ao acessar o S3: {str(e)}")
        return False

def fetch_with_retry():
    attempt = 0
    while attempt < ENV_CONFIG["MAX_RETRIES"]:
        try:
            response = requests.get(ENV_CONFIG["URL"])
            response.raise_for_status()
            return response
        except Exception as e:
            attempt += 1
            print(f"🔴 Tentativa {attempt}/{ENV_CONFIG['MAX_RETRIES']} falhou: {str(e)}")
            if attempt < ENV_CONFIG["MAX_RETRIES"]:
                print("🕒 Nova tentativa em 10 minutos...")
                time.sleep(600)
    return None

def fetch_and_save():
    print("\n🚀 Iniciando processo de coleta de dados...")
    response = fetch_with_retry()
    
    if response:
        # Alterado para salvar com ano-mês-dia-hora-minuto
        filename = f"response_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(response.json(), file, ensure_ascii=False, indent=4)
            print(f"📁 Dados salvos localmente em {filename}")
            
            if upload_to_s3(filename):
                print("🎉 Processo concluído com sucesso!")
            else:
                print("⚠️ Arquivo não foi enviado ao S3.")
        except Exception as e:
            print(f"🔴 Erro ao salvar/enviar dados: {str(e)}")
    else:
        print("🔴 Todas as tentativas falharam. Abortando processo.")

def main():
    validate_env()
    
    print(f'''
    🌟 Configurações carregadas:
    - URL: {ENV_CONFIG["URL"]}
    - Intervalo entre execuções: {ENV_CONFIG["SCHEDULE_INTERVAL_HOURS"]} horas
    - Bucket S3: {ENV_CONFIG["S3_BUCKET_NAME"]}
    - Tentativas máximas: {ENV_CONFIG["MAX_RETRIES"]}
    ''')

    schedule.every(ENV_CONFIG["SCHEDULE_INTERVAL_HOURS"]).hours.do(fetch_and_save)
    
    print("⏳ Agendamento iniciado. Aguardando para coletar dados...")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
