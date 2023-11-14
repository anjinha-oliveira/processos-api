# Raspagem de dados

Esse projeto consite na criação de uma API que busque dados de um processo em todos os graus dos Tribunais de Justiça de Alagoas (TJAL) e do Ceará (TJCE)

Para isso foi necessário desenvolver crawlers para a coleta desses dados em suas respectivas urls.

### Como instalar
```sh
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

### Para executar testes (Executar no repo **app**):

```sh
$ python3 -m pytest -v
```

### Para executar API (Executar comando no **root** do projeto):

```sh
$ python3 -m uvicorn main:app --reload --app-dir=app
```

### Tecnologias usadas

* Python3 (Versão 3.12)
* Fastapi
* Pytest
* Selenium
* Postman


### Documentação da API
http://localhost:8000/docs/


### Executanto a API pelo terminal
```sh
$ curl -X 'POST' \
  'http://localhost:8000/buscar' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "cnj": "0070337-91.2008.8.06.0001"
  }'
```