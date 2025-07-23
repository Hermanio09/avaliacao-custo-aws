import boto3
import time
from dotenv import load_dotenv
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, EndpointConnectionError
import logging

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter as credenciais e região da AWS a partir do .env
aws_region = os.getenv("AWS_REGION")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

# Configuração do logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configuração do cliente AWS com boto3
ec2_client = boto3.client('ec2',
                          region_name=aws_region,
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)

# Definir limite de custo (em termos fictícios para exemplo)
COST_THRESHOLD = 0.01  # Limite de custo (substitua com um valor real)
CHECK_INTERVAL = 60  # Intervalo para verificar instâncias (em segundos)
INSTANCE_CHECK_INTERVAL = 5  # Intervalo entre verificações de cada instância (em segundos)

# Função para verificar o custo da instância EC2 (exemplo fictício)
def check_instance_cost(instance_id):
    # Exemplo fictício de custo - substitua com o cálculo real de custo
    current_cost = 0.01  # Substitua com uma consulta real de custo
    logging.info(f"Verificando custo da instância {instance_id}: Custo atual - {current_cost}")

    if current_cost >= COST_THRESHOLD:
        logging.info(f"Custo da instância {instance_id} ultrapassou o limite. Parando a instância.")
        stop_instance(instance_id)
    else:
        logging.info(f"O custo da instância {instance_id} está abaixo do limite.")

# Função para parar a instância EC2
def stop_instance(instance_id):
    try:
        ec2_client.stop_instances(InstanceIds=[instance_id])
        logging.info(f"Instância {instance_id} parada com sucesso.")
    except NoCredentialsError:
        logging.error("Credenciais não encontradas. Verifique suas variáveis de ambiente.")
    except PartialCredentialsError:
        logging.error("Credenciais incompletas. Verifique suas variáveis de ambiente.")
    except EndpointConnectionError:
        logging.error("Falha de conexão com o endpoint da AWS. Verifique sua rede.")
    except Exception as e:
        logging.error(f"Ocorreu um erro ao tentar parar a instância {instance_id}: {e}")

# Função principal para monitorar as instâncias EC2
def monitor_ec2():
    while True:  # Loop infinito
        try:
            # Lista as instâncias EC2
            logging.info("Iniciando a verificação das instâncias EC2...")
            response = ec2_client.describe_instances()
            instances = response.get('Reservations', [])

            if not instances:
                logging.info("Nenhuma instância EC2 encontrada.")
                time.sleep(CHECK_INTERVAL)
                continue

            for reservation in instances:
                for instance in reservation['Instances']:
                    instance_id = instance['InstanceId']
                    logging.info(f"Verificando a instância {instance_id}...")
                    check_instance_cost(instance_id)
                    time.sleep(INSTANCE_CHECK_INTERVAL)  # Aguarda 5 segundos entre verificações

            logging.info(f"Aguardando {CHECK_INTERVAL} segundos antes da próxima verificação.")
            time.sleep(CHECK_INTERVAL)  # Aguarda um intervalo maior antes de verificar novamente

        except EndpointConnectionError:
            logging.error("Falha de conexão com o endpoint da AWS. Verifique sua rede.")
            time.sleep(CHECK_INTERVAL)  # Espera antes de tentar novamente
        except Exception as e:
            logging.error(f"Ocorreu um erro inesperado: {e}")
            time.sleep(CHECK_INTERVAL)  # Aguarda antes de tentar novamente

if __name__ == "__main__":
    monitor_ec2()
