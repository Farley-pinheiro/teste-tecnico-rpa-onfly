import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv() 

def send_file_to_webhook(file_path: str) -> None:
    """
    Envia um arquivo local para o webhook via requisição HTTP POST.
    """
    try:
        webhook_url = os.getenv("WEBHOOK_URL")
        username = os.getenv("WEBHOOK_USER")
        password = os.getenv("WEBHOOK_PASS")
        
        if not webhook_url or not username or not password:
            raise ValueError("Variáveis WEBHOOK_URL, WEBHOOK_USER ou WEBHOOK_PASS ausentes no .env")
        
        logging.info(f"Preparando envio seguro do arquivo '{file_path}'...")
        
        with open(file_path, 'rb') as file:
            file_payload = {'file': file}
            
            response = requests.post(
                webhook_url, 
                auth=(username, password), 
                files=file_payload,
                timeout=30
            )
            
        response.raise_for_status()
        logging.info(f"Arquivo enviado com SUCESSO! Status Code: {response.status_code}")
        
    except Exception as e:
        logging.error(f"Falha ao realizar POST no webhook: {e}")
        raise