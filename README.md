Como executar no root do projeto:

```sh
$ python3 -m uvicorn main:app --reload --app-dir=app
```

Para rodar os testes é preciso estar no repo *app*:

```sh
$ python3 -m pytest -v
```

Para utilizar o scrapy shell:

```sh
$ scrapy shell 'url do processo'
```