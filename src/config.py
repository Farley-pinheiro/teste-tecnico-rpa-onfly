"""Módulo de configurações centrais da automação."""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    Centraliza as configurações e variáveis de ambiente do projeto.

    Attributes:
        webhook_url (str): URL de destino do webhook.
        webhook_user (str): Usuário para autenticação básica no webhook.
        webhook_pass (str): Senha para autenticação básica no webhook.
        api_base_url (str): URL base da API REST Countries.
        api_timeout_s (int): Tempo limite (em segundos) para requisições na API.
    """
    
    webhook_url = os.getenv("WEBHOOK_URL")
    webhook_user = os.getenv("WEBHOOK_USER")
    webhook_pass = os.getenv("WEBHOOK_PASS")
    
    api_base_url = "https://restcountries.com/v3.1/name"
    api_timeout_s = 10
    
    def validate(self) -> None:
        """
        Valida se as variáveis obrigatórias estão presentes antes de iniciar o robô.

        Raises:
            ValueError: Se alguma das credenciais ou URLs obrigatórias não for encontrada no arquivo .env.
        """
        missing = []
        if not self.webhook_url: missing.append("WEBHOOK_URL")
        if not self.webhook_user: missing.append("WEBHOOK_USER")
        if not self.webhook_pass: missing.append("WEBHOOK_PASS")
        
        if missing:
            raise ValueError(f"Erro Crítico: Variáveis ausentes no arquivo .env: {', '.join(missing)}")