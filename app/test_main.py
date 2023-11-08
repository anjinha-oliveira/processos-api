from fastapi.testclient import TestClient
from unittest.mock import patch

from .main import app

client = TestClient(app)

@patch('app.main.RasparTjal', return_value={
    "area": "Cível",
    "assunto": "Dano Material",
    "classe": "Procedimento Comum Cível",
    "cnj": "0710802-55.2018.8.02.0001",
    "data_de_distribuicao": "02/05/2018",
    "juiz": "José Cícero Alves da Silva",
    "valor_da_acao": "281.178,42",

})
def test_garante_que_recebemos_todas_informacoes(mocked_RasparTjal):
    resposta = client.post(
        "/buscar",
        json={"cnj": "0710802-55.2018.8.02.0001"},
    )
    assert resposta.status_code == 200
    assert resposta.json() == {
        "processo": {
            "cnj": "0710802-55.2018.8.02.0001",
            "classe": "Procedimento Comum Cível",
            "area": "Cível",
            "assunto": "Dano Material",
            "data_de_distribuicao": "02/05/2018",
            "juiz": "José Cícero Alves da Silva",
            "valor_da_acao": "281.178,42",
            # "partes-do-processo": {
                # "autor": {
                    # "nome": "José Carlos Cerqueira Souza Filho",
                    # "advogados": [
                        # "Vinicius Faria de Cerqueira"
                    # ],
                # },
                # "reu": {
                    # "nome": "Cony Engenharia Ltda.",
                    # "advogados": [
                        # "Carlos Henrique de Mendonça Brandão",
                        # "Guilherme Freire Furtado",
                        # "Maria Eugênia Barreiros de Mello",
                        # "Vítor Reis de Araujo Carvalho",
                    # ]
                # }
            # },
            # "movimentacoes": [
                # {
                    # "data": "24/08/2023",
                    # "movimento": "Arquivado Definitivamente"
                # }
            # ]
        }
    }

def test_garante_que_cnj_não_seja_vazio():
    resposta = client.post(
        "/buscar",
        json={"cnj": ""}
    )
    assert resposta.status_code == 400
    assert resposta.json() == {
        "message":"Cnj vazio."
    }