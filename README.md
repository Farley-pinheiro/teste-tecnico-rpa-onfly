# Teste Técnico RPA - Coleta e Integração de Dados

Este projeto é uma automação em Python (RPA) desenvolvida para um teste técnico. O robô realiza web scraping para identificar os países com a maior média de idade e, em seguida, consome uma API pública para enriquecer os dados com informações de capital, idiomas e moedas, enviando o resultado consolidado via webhook HTTP.

## Arquitetura e Padrões de Projeto

O projeto foi rigorosamente modularizado visando separação de responsabilidades, segurança, performance e resiliência a falhas de rede:

* `src/config.py`: Centralização das variáveis de ambiente (`Settings`) com validação *Fail-Fast* na inicialização.
* `src/web_scraper.py`: Navegação *headless* via Playwright e extração de tabelas HTML utilizando Pandas.
* `src/data_processor.py`: Limpeza de dados (*Data Cleansing*), tratamento de valores nulos e regras de negócio.
* `src/api_client.py`: Integração com a REST Countries API utilizando **Session Pooling** (reutilização de conexão para chamadas em lote) e tratamento de exceções com **Retry/Backoff**.
* `src/webhook_sender.py`: Envio do arquivo gerado via requisição POST com autenticação Basic Auth, utilizando **Injeção de Dependência** para receber as configurações e sistema de tentativas para instabilidades de rede.
* `main.py`: Orquestrador central com sistema de **Logging Rastreável** (incluindo nome do módulo e linha) para monitoramento de ponta a ponta.

**Destaques Técnicos:**
- Tratamento de exceções com lógica de *Retry* e *Backoff Exponencial* (nativa) nas requisições HTTP.
- *Docstrings* padronizadas no formato **Google Style** 
- *Loggers* instanciados por módulo (`logging.getLogger(__name__)`) evitando poluição de logs de bibliotecas de terceiros.

## Tecnologias Utilizadas

* **Python 3.x**
* **Playwright:** Web scraping moderno e robusto.
* **Pandas:** Manipulação de DataFrames e exportação limpa para Excel (`.xlsx`).
* **Requests:** Consumo de APIs REST e envio de Webhooks com gerenciamento de Sessão (`requests.Session`).
* **python-dotenv:** Gerenciamento seguro de credenciais em ambiente local.

## Como executar o projeto

```bash
1. Clone este repositório:

git clone https://github.com/Farley-pinheiro/teste-tecnico-rpa-onfly

2. Instale as dependências do projeto:

pip install -r requirements.txt

3. Instale os navegadores do Playwright:

playwright install

4. Configuração de Ambiente (Importante):

Crie um arquivo oculto chamado .env na raiz do projeto e adicione as credenciais fornecidas no teste. O robô validará essas chaves antes de iniciar:

WEBHOOK_URL=url
WEBHOOK_USER=usuario
WEBHOOK_PASS=senha

5. Execute o orquestrador:

python main.py

O robô fará a execução segura gerando o arquivo Excel Teste RPA - Farley Pinheiro dos Santos.xlsx, enviará automaticamente para o webhook e registrará a auditoria detalhada no arquivo de texto execucao_robo.log.
