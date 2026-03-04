import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv() 

def enviar_arquivo_webhook(nome_arquivo: str) -> None:
    """
    Envia um arquivo local para o webhook via requisição HTTP POST.

    Utiliza autenticação Basic Auth com credenciais carregadas de forma segura 
    através de variáveis de ambiente (WEBHOOK_USER e WEBHOOK_PASS).

    Args:
        nome_arquivo (str): O caminho (relativo ou absoluto) do arquivo a ser enviado.

    Raises:
        Exception: Levanta a exceção caso ocorra algum erro na comunicação com o servidor,
                   repassando o erro para o orquestrador principal.
    """
    url_webhook = os.getenv("WEBHOOK_URL")
    usuario = os.getenv("WEBHOOK_USER")
    senha = os.getenv("WEBHOOK_PASS")
    
    if not url_webhook or not usuario or not senha:
        logging.error("Configurações do webhook não encontradas! Verifique o arquivo .env.")
        raise ValueError("Variáveis WEBHOOK_URL, WEBHOOK_USER ou WEBHOOK_PASS ausentes.")
    
    logging.info(f"Preparando envio seguro do arquivo '{nome_arquivo}'...")
    
    try:
        with open(nome_arquivo, 'rb') as arquivo:
            payload_arquivo = {'file': arquivo}
            
            resposta = requests.post(
                url_webhook, 
                auth=(usuario, senha), 
                files=payload_arquivo
            )
            
        resposta.raise_for_status()
        logging.info(f"Arquivo enviado com SUCESSO! Status Code: {resposta.status_code}")
        
    except Exception as e:
        logging.error(f"Falha ao realizar POST no webhook: {e}")
        raise