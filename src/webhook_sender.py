"""Módulo responsável pelo envio de dados via webhooks HTTP."""

import logging
import requests
import time

from src.config import Settings

logger = logging.getLogger(__name__)

_MAX_RETRIES = 3
_RETRY_BACKOFF = 3.0  # segundos

def send_file_to_webhook(file_path: str, settings: Settings) -> None:
    """
    Envia um arquivo local para o webhook via requisição HTTP POST.

    Inclui lógica de Retry/Backoff Exponencial simplificado para lidar com instabilidades na rede.

    Args:
        file_path (str): O caminho (relativo ou absoluto) do arquivo a ser enviado.
        settings (Settings): Instância de configurações contendo a URL e credenciais do Webhook.

    Raises:
        Exception: Erro de rede ou HTTP após todas as tentativas falharem.
    """
    logger.info("Preparando envio seguro do arquivo '%s'...", file_path)
    
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            with open(file_path, 'rb') as file:
                file_payload = {'file': file}
                
                response = requests.post(
                    settings.webhook_url, 
                    auth=(settings.webhook_user, settings.webhook_pass), 
                    files=file_payload,
                    timeout=30
                )
                
            response.raise_for_status()
            logger.info("Arquivo enviado com SUCESSO! Status Code: %d", response.status_code)
            return
            
        except requests.RequestException as exc:
            if attempt < _MAX_RETRIES:
                sleep_time = _RETRY_BACKOFF * attempt
                logger.warning("Tentativa %d/%d de envio falhou. Tentando novamente em %ds... (Erro: %s)", 
                               attempt, _MAX_RETRIES, sleep_time, exc)
                time.sleep(sleep_time)
            else:
                logger.error("Falha definitiva ao realizar POST no webhook após %d tentativas.", _MAX_RETRIES)
                raise
                
        except Exception as exc:
            logger.error("Erro inesperado no envio do webhook: %s", exc)
            raise