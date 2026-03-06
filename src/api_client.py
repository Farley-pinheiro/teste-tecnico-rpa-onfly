import logging
import time
import requests

from typing import Optional
from requests import Session, HTTPError
from src.config import Settings

logger = logging.getLogger(__name__)

_FALLBACK = {"Capital": "N/A", "Linguagens": "N/A", "Moedas": "N/A"}
_MAX_RETRIES = 3
_RETRY_BACKOFF = 2.0  # segundos

def _normalize_name(name: str) -> str:
    """Normaliza o nome do país para a API."""
    return name.replace(" & ", " and ").split(" (")[0].strip()

def fetch_api_data(
    country_name: str,
    settings: Settings,
    session: Optional[Session] = None,
) -> dict:
    """
    Consulta a REST Countries API para um país.
    Reutiliza sessão HTTP se fornecida (recomendado para chamadas em lote).
    """
    http = session or requests
    normalized = _normalize_name(country_name)
    url = f"{settings.api_base_url}/{normalized}?fullText=false"
    
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            response = http.get(url, timeout=settings.api_timeout_s)
            response.raise_for_status()
            data = response.json()[0]
            
            capital = (data.get("capital") or ["N/A"])[0]
            languages = ", ".join(data.get("languages", {}).values()) or "N/A"
            currencies = ", ".join(
                info.get("name", "N/A") for info in data.get("currencies", {}).values()
            ) or "N/A"
            
            logger.info("API OK: %s -> Capital=%s", country_name, capital)
            return {"Capital": capital, "Linguagens": languages, "Moedas": currencies}
            
        except HTTPError as exc:
            if exc.response is not None and exc.response.status_code == 404:
                logger.warning("País não encontrado na API: %s", country_name)
                return _FALLBACK.copy()
            logger.warning("Tentativa %d/%d falhou para %s: %s", attempt, _MAX_RETRIES, country_name, exc)
            
        except Exception as exc:
            logger.warning("Tentativa %d/%d falhou para %s: %s", attempt, _MAX_RETRIES, country_name, exc)
            
        if attempt < _MAX_RETRIES:
            time.sleep(_RETRY_BACKOFF * attempt)
            
    logger.error("Todas as tentativas falharam para: %s", country_name)
    return _FALLBACK.copy()

def fetch_all_countries(countries: list[str], settings: Settings) -> list[dict]:
    """Busca dados para uma lista de países reutilizando a mesma sessão HTTP."""
    logger.info("Iniciando busca em lote de %d países com Session Pooling...", len(countries))
    with requests.Session() as session:
        return [fetch_api_data(c, settings, session) for c in countries]