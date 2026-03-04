import pandas as pd
import logging

def tratar_e_filtrar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpa o DataFrame bruto, renomeia colunas, remove valores nulos e filtra o top 10.

    Args:
        df (pd.DataFrame): DataFrame bruto contendo os dados extraídos do scraping.

    Returns:
        pd.DataFrame: DataFrame contendo apenas os 10 países com a maior média de idade, 
                      com as colunas formatadas ('País', 'Qtd habitantes', 'Média idade').
    """
    logging.info("Iniciando o tratamento e limpeza dos dados brutos...")
    
    colunas_interesse = {
        'Country (or dependency)': 'País',
        df.filter(like='Population').columns[0]: 'Qtd habitantes',
        'Median Age': 'Média idade'
    }
    
    df_limpo = df.rename(columns=colunas_interesse)[list(colunas_interesse.values())]
    
    df_limpo = df_limpo[df_limpo['Média idade'] != 'N.A.']
    df_limpo['Média idade'] = pd.to_numeric(df_limpo['Média idade'], errors='coerce')
    
    linhas_antes = len(df_limpo)
    df_limpo = df_limpo.dropna(subset=['Média idade'])
    linhas_depois = len(df_limpo)
    
    if linhas_antes != linhas_depois:
        logging.info(f"Removidas {linhas_antes - linhas_depois} linhas com média de idade inválida/nula.")
    
    top_10 = df_limpo.nlargest(10, 'Média idade')
    return top_10