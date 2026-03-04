import requests
import logging

def buscar_dados_api(nome_pais: str) -> dict:
    """
    Consome a API REST Countries para buscar informações adicionais de um país.

    Realiza o tratamento prévio do nome do país (substituindo '&' por 'and' e removendo
    textos entre parênteses) para garantir a compatibilidade com os endpoints da API.

    Args:
        nome_pais (str): O nome do país em inglês, conforme extraído da base de dados.

    Returns:
        dict: Um dicionário contendo as chaves 'Capital', 'Linguagens' e 'Moedas'.
              Em caso de falha na requisição, retorna os mesmos campos preenchidos com 'N/A'.
    """
    nome_pais_tratado = nome_pais.replace(' & ', ' and ')
    nome_busca = nome_pais_tratado.split(' (')[0]
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
        logging.error(f"Erro ao buscar dados na API para '{nome_pais}': {e}")
        return {'Capital': 'N/A', 'Linguagens': 'N/A', 'Moedas': 'N/A'}