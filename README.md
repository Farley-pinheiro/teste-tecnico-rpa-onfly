# Teste Técnico RPA - Coleta e Integração de Dados

Este projeto é uma automação em Python (RPA) desenvolvida para um teste técnico. O robô realiza web scraping para identificar os países com a maior média de idade e, em seguida, consome uma API pública para enriquecer os dados com informações de capital, idiomas e moedas.

## Arquitetura do Projeto 

O projeto foi modularizado visando a separação de responsabilidades, segurança e resiliência:
* `extrator_web.py`: Navegação web (Playwright) e extração de tabelas HTML (Pandas).
* `processador_dados.py`: Limpeza de dados (Data Cleansing) e regras de negócio.
* `consumidor_api.py`: Integração com a REST Countries API e tratamento de exceções.
* `enviar_webhook.py`: Envio do arquivo gerado para o webhook via POST com Basic Auth, utilizando variáveis de ambiente para omitir credenciais do código-fonte.
* `main.py`: O orquestrador central com sistema de **Logging** implementado para rastreabilidade de ponta a ponta.

## Tecnologias Utilizadas

* **Python 3.x**
* **Playwright:** Web scraping robusto.
* **Pandas:** Manipulação de DataFrames e exportação para `.xlsx`.
* **Requests:** Consumo de APIs REST e envio de Webhooks.
* **python-dotenv:** Gerenciamento seguro de credenciais via variáveis de ambiente.
* **Logging (Nativo):** Auditoria e geração de logs de execução (`execucao_robo.log`).

## Como executar o projeto

```bash
1. Clone este repositório:

git clone https://github.com/Farley-pinheiro/teste-tecnico-rpa-onfly

2. Instale as dependências do projeto:

pip install -r requirements.txt

3. Instale os navegadores do Playwright:

playwright install

4. Configuração de Ambiente (Importante):

Crie um arquivo chamado .env na raiz do projeto e adicione as credenciais solicitadas no arquivo `enviar_webhook.py`.

5. Execute o orquestrador:

python main.py

O robô gerará o arquivo Excel, fará o envio automático para o webhook e criará um arquivo execucao_robo.log com o detalhamento de cada etapa.

