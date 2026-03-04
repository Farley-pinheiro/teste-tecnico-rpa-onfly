import pandas as pd

def tratar_e_filtrar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpa os dados, removendo valores nulos e retorna os 10 maiores.
    """
    colunas_interesse = {
        'Country (or dependency)': 'País',
        df.filter(like='Population').columns[0]: 'Qtd habitantes',
        'Median Age': 'Média idade'
    }
    
    df_limpo = df.rename(columns=colunas_interesse)[list(colunas_interesse.values())]
    
    df_limpo = df_limpo[df_limpo['Média idade'] != 'N.A.']
    df_limpo['Média idade'] = pd.to_numeric(df_limpo['Média idade'], errors='coerce')
    
    df_limpo = df_limpo.dropna(subset=['Média idade'])
    
    top_10 = df_limpo.nlargest(10, 'Média idade')
    return top_10