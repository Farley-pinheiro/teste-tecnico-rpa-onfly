import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Centraliza as configurações e variáveis de ambiente do projeto."""
    
    webhook_url = os.getenv("WEBHOOK_URL")
    webhook_user = os.getenv("WEBHOOK_USER")
    webhook_pass = os.getenv("WEBHOOK_PASS")
    
    api_base_url = "https://restcountries.com/v3.1/name"
    api_timeout_s = 10
    
    def validate(self):
        """Valida se as variáveis obrigatórias estão presentes antes de iniciar o robô."""
        missing = []
        if not self.webhook_url: missing.append("WEBHOOK_URL")
        if not self.webhook_user: missing.append("WEBHOOK_USER")
        if not self.webhook_pass: missing.append("WEBHOOK_PASS")
        
        if missing:
            raise ValueError(f"Erro Crítico: Variáveis ausentes no arquivo .env: {', '.join(missing)}")