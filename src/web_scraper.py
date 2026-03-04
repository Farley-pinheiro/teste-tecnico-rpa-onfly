import pandas as pd
import logging
from playwright.sync_api import sync_playwright
from io import StringIO

def extract_table_data(target_url: str) -> pd.DataFrame:
    """
    Acessa a página web informada utilizando o Playwright e extrai a tabela principal.

    Args:
        target_url (str): A URL da página web que contém a tabela de dados.

    Returns:
        pd.DataFrame: Um DataFrame Pandas contendo os dados brutos da primeira tabela.
    """
    logging.info(f"Iniciando navegação headless para a URL: {target_url}")
    
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(target_url, timeout=60000) 
            
            html_content = page.content()
            browser.close()
            logging.info("Navegação concluída e HTML extraído com sucesso.")
            
        tables = pd.read_html(StringIO(html_content))
        main_df = tables[0]
        
        return main_df
        
    except Exception as e:
        logging.error(f"Falha ao extrair dados da web. Detalhes: {e}")
        raise