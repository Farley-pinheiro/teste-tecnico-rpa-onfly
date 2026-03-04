"""
Orquestrador principal da automação de RPA.
Responsável por coordenar a extração, tratamento, consumo de API,
consolidação e envio dos dados populacionais e informações de países.
"""
import pandas as pd
import logging
import sys

from src.web_scraper import extract_table_data
from src.data_processor import process_and_filter_data
from src.api_client import fetch_api_data
from src.webhook_sender import send_file_to_webhook

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("execucao_robo.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

def main() -> None:
    """Função principal que orquestra o fluxo do robô."""
    logging.info("--- Iniciando automação de coleta de dados (Worldometers) ---")
    
    try:
        target_url = "https://www.worldometers.info/world-population/population-by-country/"
        
        logging.info("Etapa 1: Acessando a página e extraindo a tabela HTML...")
        raw_df = extract_table_data(target_url)
        
        logging.info("Etapa 2: Tratando dados e filtrando o Top 10 maiores médias de idade...")
        top_10_df = process_and_filter_data(raw_df)
        logging.info(f"Top 10 processado com sucesso! {len(top_10_df)} países encontrados.")
        
        logging.info("Etapa 3: Buscando informações adicionais na API (REST Countries)...")
        additional_data = []
        
        for _, row in top_10_df.iterrows():
            country = row['País']
            logging.info(f"   -> Consultando dados para: {country}...")
            api_info = fetch_api_data(country)
            additional_data.append(api_info)
            
        logging.info("Etapa 4: Consolidando os dados em um arquivo Excel...")
        api_df = pd.DataFrame(additional_data)
        final_df = pd.concat([top_10_df.reset_index(drop=True), api_df.reset_index(drop=True)], axis=1)
        
        output_filename = "Teste RPA - Farley Pinheiro dos Santos.xlsx"
        final_df.to_excel(output_filename, index=False)
        logging.info(f"Arquivo '{output_filename}' gerado com sucesso.")
        
        logging.info("Etapa 5: Enviando arquivo para o webhook...")
        send_file_to_webhook(output_filename)
        
        logging.info("--- Automação finalizada com SUCESSO! ---")

    except Exception as e:
        logging.critical(f"ERRO FATAL: A automação falhou e foi interrompida. Detalhes: {e}", exc_info=True)

if __name__ == "__main__":
    main()