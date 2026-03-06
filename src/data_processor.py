"""Módulo responsável pelo tratamento e limpeza de dados populacionais."""

import pandas as pd
import logging

logger = logging.getLogger(__name__)

def process_and_filter_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpa o DataFrame bruto, renomeia colunas, remove valores nulos e filtra o top 10.

    Args:
        raw_df (pd.DataFrame): DataFrame bruto contendo os dados extraídos do scraping.

    Returns:
        pd.DataFrame: DataFrame contendo apenas os 10 países com a maior média de idade.

    Raises:
        Exception: Falha caso os dados brutos não contenham as colunas esperadas.
    """
    logger.info("Iniciando o tratamento e limpeza dos dados brutos...")
    
    try:
        target_columns = {
            'Country (or dependency)': 'País',
            raw_df.filter(like='Population').columns[0]: 'Qtd habitantes',
            'Median Age': 'Média idade'
        }
        
        cleaned_df = raw_df.rename(columns=target_columns)[list(target_columns.values())]
        
        cleaned_df = cleaned_df[cleaned_df['Média idade'] != 'N.A.']
        cleaned_df['Média idade'] = pd.to_numeric(cleaned_df['Média idade'], errors='coerce')
        
        rows_before = len(cleaned_df)
        cleaned_df = cleaned_df.dropna(subset=['Média idade'])
        rows_after = len(cleaned_df)
        
        if rows_before != rows_after:
            logger.info("Removidas %d linhas com média de idade inválida/nula.", (rows_before - rows_after))
        
        top_10_df = cleaned_df.nlargest(10, 'Média idade')
        return top_10_df
        
    except Exception as exc:
        logger.error("Falha no processamento (Data Cleansing) dos dados: %s", exc)
        raise