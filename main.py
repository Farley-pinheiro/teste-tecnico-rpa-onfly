"""
Orquestrador principal da automação de RPA.
Responsável por coordenar a extração, tratamento, consumo de API,
consolidação e envio dos dados populacionais e informações de países.
"""
import pandas as pd
import logging
import sys

from extrator_web import extrair_dados_tabela
from processador_dados import tratar_e_filtrar_dados
from consumidor_api import buscar_dados_api
from enviar_webhook import enviar_arquivo_webhook

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("execucao_robo.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

def main() -> None:
    """
    Função principal que orquestra o fluxo do robô.
    
    Etapas:
    1. Extrai a tabela de população do Worldometers.
    2. Filtra os 10 países com maior média de idade.
    3. Busca dados de capital, idioma e moeda na REST Countries API.
    4. Consolida os dados e salva em um arquivo Excel (.xlsx).
    5. Envia o arquivo resultante via webhook.
    """
    logging.info("--- Iniciando automação de coleta de dados (Worldometers) ---")
    
    try:
        url_alvo = "https://www.worldometers.info/world-population/population-by-country/"
        
        logging.info("Etapa 1: Acessando a página e extraindo a tabela HTML...")
        df_bruto = extrair_dados_tabela(url_alvo)
        
        logging.info("Etapa 2: Tratando dados e filtrando o Top 10 maiores médias de idade...")
        df_top_10 = tratar_e_filtrar_dados(df_bruto)
        logging.info(f"Top 10 processado com sucesso! {len(df_top_10)} países encontrados.")
        
        logging.info("Etapa 3: Buscando informações adicionais na API (REST Countries)...")
        dados_adicionais = []
        
        for _, linha in df_top_10.iterrows():
            pais = linha['País']
            logging.info(f"   -> Consultando dados para: {pais}...")
            info_api = buscar_dados_api(pais)
            dados_adicionais.append(info_api)
            
        logging.info("Etapa 4: Consolidando os dados em um arquivo Excel...")
        df_api = pd.DataFrame(dados_adicionais)
        df_final = pd.concat([df_top_10.reset_index(drop=True), df_api.reset_index(drop=True)], axis=1)
        
        nome_arquivo = "Teste RPA - Farley Pinheiro dos Santos.xlsx"
        df_final.to_excel(nome_arquivo, index=False)
        logging.info(f"Arquivo '{nome_arquivo}' gerado com sucesso.")
        
        logging.info("Etapa 5: Enviando arquivo para o webhook...")
        enviar_arquivo_webhook(nome_arquivo)
        
        logging.info("--- Automação finalizada com SUCESSO! ---")

    except Exception as e:
        logging.critical(f"ERRO FATAL: A automação falhou e foi interrompida. Detalhes: {e}", exc_info=True)

if __name__ == "__main__":
    main()