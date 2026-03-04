import requests

def buscar_dados_api(nome_pais: str) -> dict:
    """
    Consome a API para buscar Capital, Linguagens e Moedas.
    """
    nome_pais = nome_pais.replace(' & ', ' and ')
    nome_busca = nome_pais.split(' (')[0]
    url = f"https://restcountries.com/v3.1/name/{nome_busca}"
    
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        
        dados = resposta.json()[0]
        
        capital = dados.get('capital', ['N/A'])[0]
        
        linguagens = dados.get('languages', {})
        linguagens_str = ", ".join(linguagens.values()) if linguagens else "N/A"
        
        moedas = dados.get('currencies', {})
        moedas_str = ", ".join([info.get('name', 'N/A') for info in moedas.values()]) if moedas else "N/A"
        
        return {
            'Capital': capital,
            'Linguagens': linguagens_str,
            'Moedas': moedas_str            
        }
        
    except Exception as e:
        print(f'Erro ao buscar dados para {nome_pais}: {e}')
        return {'Capital': 'N/A', 'Linguagens': 'N/A', 'Moedas': 'N/A'}