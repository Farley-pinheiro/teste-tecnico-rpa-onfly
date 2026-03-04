import requests
import logging

def fetch_api_data(country_name: str) -> dict:
    """
    Consome a API REST Countries para buscar informações adicionais de um país.

    Args:
        country_name (str): O nome do país em inglês.

    Returns:
        dict: Um dicionário contendo as chaves 'Capital', 'Linguagens' e 'Moedas'.
              Em caso de falha na requisição, retorna preenchido com 'N/A'.
    """
    try:
        treated_country_name = country_name.replace(' & ', ' and ')
        search_name = treated_country_name.split(' (')[0].strip() 
        endpoint_url = f"https://restcountries.com/v3.1/name/{search_name}"
        
        response = requests.get(endpoint_url, timeout=10)
        response.raise_for_status()
        
        country_data = response.json()[0]
        
        capital = country_data.get('capital', ['N/A'])[0]
        
        languages = country_data.get('languages', {})
        languages_str = ", ".join(languages.values()) if languages else "N/A"
        
        currencies = country_data.get('currencies', {})
        currencies_str = ", ".join([info.get('name', 'N/A') for info in currencies.values()]) if currencies else "N/A"
        
        return {
            'Capital': capital,
            'Linguagens': languages_str,
            'Moedas': currencies_str            
        }
        
    except Exception as e:
        logging.error(f"Erro ao buscar dados na API para '{country_name}': {e}")
        return {'Capital': 'N/A', 'Linguagens': 'N/A', 'Moedas': 'N/A'}