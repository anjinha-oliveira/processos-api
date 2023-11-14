# Raspagem de dados

Esse projeto consite na criação de uma API que busque dados de um processo em todos os graus dos Tribunais de Justiça de Alagoas (TJAL) e do Ceará (TJCE)

Para isso foi necessário desenvolver crawlers para a coleta desses dados em suas respectivas urls.

### Tecnologias usadas

* Python3
* Fastapi
* Pytest
* Selenium
* Postman

Para executar API (Executar comando no **root** do projeto):

```sh
$ python3 -m uvicorn main:app --reload --app-dir=app
```

Para executar testes (Executar no repo **app**):

```sh
$ python3 -m pytest -v
```

#### Rota de requisição POST:

* localhost:8000/buscar/