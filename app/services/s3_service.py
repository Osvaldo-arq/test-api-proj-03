import boto3
import logging
import os
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

load_dotenv()

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.input_bucket = os.getenv("INPUT_BUCKET")
        self.output_bucket = os.getenv("OUTPUT_BUCKET")

        if not self.input_bucket or not self.output_bucket:
            raise ValueError("As variáveis INPUT_BUCKET e OUTPUT_BUCKET não estão definidas!")

    def upload_file(self, file_bytes, file_name):
        """
        Faz upload do arquivo para o INPUT_BUCKET.
        """
        try:
            self.s3_client.put_object(Bucket=self.input_bucket, Key=file_name, Body=file_bytes)
            logger.info(f"Arquivo {file_name} salvo no INPUT_BUCKET")
        except NoCredentialsError:
            logger.error("Credenciais da AWS não encontradas!")
            raise
        except Exception as e:
            logger.error(f"Erro ao enviar arquivo para o S3: {e}")
            raise

    def upload_csv(self, file_name, csv_content):
        """
        Salva o CSV extraído no OUTPUT_BUCKET.
        """
        try:
            self.s3_client.put_object(Bucket=self.output_bucket, Key=file_name, Body=csv_content)
            logger.info(f"Arquivo {file_name} salvo no OUTPUT_BUCKET")
        except Exception as e:
            logger.error(f"Erro ao salvar CSV no S3: {e}")
            raise
