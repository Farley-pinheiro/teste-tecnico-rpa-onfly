import pandas as pd
from playwright.sync_api import sync_playwright
from io import StringIO

def extrair_dados_tabela(url: str) -> pd.DataFrame:
    """
    Acessa a página usando playwright e extrai a tabela principal usando pandas
    """
    with sync_playwright() as pw:
        navegador = pw.chromium.launch(headless=True)
        pagina = navegador.new_page()
        pagina.goto(url)
        
        html = pagina.content()
        navegador.close()
        
    tabelas = pd.read_html(StringIO(html))
    df_principal = tabelas[0]
    
    return df_principal