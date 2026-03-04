import pandas as pd
import logging

from playwright.sync_api import sync_playwright
from io import StringIO

def extrair_dados_tabela(url: str) -> pd.DataFrame:
    """
    Acessa a página web informada utilizando o Playwright e extrai a tabela principal.

    Args:
        url (str): A URL da página web que contém a tabela de dados.

    Returns:
        pd.DataFrame: Um DataFrame Pandas contendo os dados brutos da primeira tabela encontrada no HTML.
    """
    logging.info(f"Iniciando navegação headless para a URL: {url}")
    
    with sync_playwright() as pw:
        navegador = pw.chromium.launch(headless=True)
        pagina = navegador.new_page()
        pagina.goto(url)
        
        html = pagina.content()
        navegador.close()
        logging.info("Navegação concluída e HTML extraído com sucesso.")
        
    tabelas = pd.read_html(StringIO(html))
    df_principal = tabelas[0]
    
    return df_principal