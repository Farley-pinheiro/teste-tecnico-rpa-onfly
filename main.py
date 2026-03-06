"""
Orquestrador principal da automação de RPA.
Responsável por coordenar a extração, tratamento, consumo de API,
consolidação e envio dos dados populacionais e informações de países.
"""

import pandas as pd
import logging
import sys

from src.config import Settings
from src.web_scraper import extract_table_data
from src.data_processor import process_and_filter_data
from src.api_client import fetch_all_countries
from src.webhook_sender import send_file_to_webhook

# Configuração Global de Log do projeto
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(filename)s] - %(message)s',
    handlers=[
        logging.FileHandler("execucao_robo.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Logger específico do orquestrador
logger = logging.getLogger(__name__)

def main() -> None:
    """
    Função principal que orquestra o fluxo do robô.
    
    O processo consiste em extrair dados web, tratá-los, enriquecer com API externa,
    consolidar o resultado em um arquivo Excel e enviar o arquivo via webhook.
    """
    settings = Settings()
    settings.validate()
    
    logger.info("--- Iniciando automação de coleta de dados (Worldometers) ---")
    
    try:
        target_url = "https://www.worldometers.info/world-population/population-by-country/"
        
        logger.info("Etapa 1: Acessando a página e extraindo a tabela HTML...")
        raw_df = extract_table_data(target_url)
        
        logger.info("Etapa 2: Tratando dados e filtrando o Top 10 maiores médias de idade...")
        top_10_df = process_and_filter_data(raw_df)
        logger.info("Top 10 processado com sucesso! %d países encontrados.", len(top_10_df))
        
        logger.info("Etapa 3: Buscando informações adicionais na API (REST Countries)...")
        countries_list = top_10_df['País'].tolist()
        additional_data = fetch_all_countries(countries_list, settings)
            
        logger.info("Etapa 4: Consolidando os dados em um arquivo Excel...")
        api_df = pd.DataFrame(additional_data)
        final_df = pd.concat([top_10_df.reset_index(drop=True), api_df.reset_index(drop=True)], axis=1)
        
        output_filename = "Teste RPA - Farley Pinheiro dos Santos.xlsx"
        final_df.to_excel(output_filename, index=False)
        logger.info("Arquivo '%s' gerado com sucesso.", output_filename)
        
        logger.info("Etapa 5: Enviando arquivo para o webhook...")
        send_file_to_webhook(output_filename, settings)
        
        logger.info("--- Automação finalizada com SUCESSO! ---")

    except Exception as exc:
        logger.critical("ERRO FATAL: A automação falhou e foi interrompida. Detalhes: %s", exc, exc_info=True)

if __name__ == "__main__":
    main()