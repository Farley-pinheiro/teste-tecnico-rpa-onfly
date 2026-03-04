import pandas as pd

from extrator_web import extrair_dados_tabela
from processador_dados import tratar_e_filtrar_dados
from consumidor_api import buscar_dados_api

def main():
    print('Iniciando extração de dados...')
    url_alvo = "https://www.worldometers.info/world-population/population-by-country/"
    
    df_bruto = extrair_dados_tabela(url_alvo)
    
    df_top_10 = tratar_e_filtrar_dados(df_bruto)
    print('Top 10 países encontrados!\n')
    
    print('Buscando informações na API restcountries...')
    dados_adicionais = []
    
    for _, linha in df_top_10.iterrows():
        pais = linha['País']
        print(f'Consultado: {pais}...')
        info_api = buscar_dados_api(pais)
        dados_adicionais.append(info_api)
        
    df_api = pd.DataFrame(dados_adicionais)
    df_final = pd.concat([df_top_10.reset_index(drop=True), df_api.reset_index(drop=True)], axis=1)
    
    nome_arquivo = "Teste RPA - Farley Pinheiro dos Santos.xlsx"
    df_final.to_excel(nome_arquivo, index=False)
    print(f'\nProcesso concluído! Arquivo gerado.')
    
if __name__ == "__main__":
    main()