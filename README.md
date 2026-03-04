# Teste Técnico RPA - Coleta e Integração de Dados

Este projeto é uma automação em Python (RPA) desenvolvida para um teste técnico. O robô realiza web scraping para identificar os países com a maior média de idade e, em seguida, consome uma API pública para enriquecer os dados com informações de capital, idiomas e moedas.

## Arquitetura do Projeto 

O projeto foi modularizado visando a separação de responsabilidades e facilidade de manutenção:
* `extrator_web.py`: Responsável por acessar a página web e extrair a tabela HTML.
* `processador_dados.py`: Responsável por limpar os dados e aplicar as regras de negócio usando Pandas.
* `consumidor_api.py`: Responsável por consultar a REST Countries API e tratar exceções.
* `main.py`: O orquestrador que conecta todas as etapas e exporta o arquivo `.xlsx` final.

## Tecnologias Utilizadas

* **Python 3.x**
* **Playwright:** Para web scraping confiável e contorno de bloqueios dinâmicos.
* **Pandas:** Para manipulação de DataFrames e consolidação de dados.
* **Requests:** Para consumo da API REST.

## Como executar o projeto

```bash
1. Clone este repositório:

git clone https://github.com/Farley-pinheiro/teste-tecnico-rpa-onfly

2. Instale as dependências do projeto:

pip install -r requirements.txt

3. Instale os navegadores do Playwright:

playwright install

4. Execute o orquestrador:

python main.py

O robô iniciará o processo e, ao final, gerará um arquivo chamado Teste RPA - Farley Pinheiro dos Santos.xlsx na mesma pasta.

