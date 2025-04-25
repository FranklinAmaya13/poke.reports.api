import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
import logging

load_dotenv()

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_SAK")
AZURE_STORAGE_CONTAINER = os.getenv("AZURE_STORAGE_CONTAINER")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AzBlob:
    def __init__(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        self.container_client = self.blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER)

    def generate_sas(self, id: int):
        blob_name = f"poke_report_{id}.csv"
        sas_token = generate_blob_sas(
            account_name=self.blob_service_client.account_name,
            container_name=AZURE_STORAGE_CONTAINER,
            blob_name=blob_name,
            account_key=self.blob_service_client.credential.account_key,
            permission=BlobSasPermissions(read=True), 
            expiry=datetime.utcnow() + timedelta(hours=1)
        )
        return sas_token
    
    def delete_csv(self, id: int):
        blob_name = f"poke_report_{id}.csv"
        try:
            self.container_client.delete_blob(blob_name)
            logger.info(f"Archivo '{blob_name}' eliminado correctamente.")

        except Exception as e:
            logger.error(f"Error al eliminar '{blob_name}': {e}")