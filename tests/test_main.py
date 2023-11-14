from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

client = TestClient(app)

resultado_RasparTjal = {
    "cnj": "0710802-55.2018.8.02.0001",
    "classe": "Procedimento Comum Cível",
    "area": "Cível",
    "assunto": "Dano Material",
    "data_de_distribuicao": "02/05/2018",
    "juiz": "José Cícero Alves da Silva",
    "valor_da_acao": "281.178,42",
    "partes-do-processo": {
        "autor": {
            "nome": "José Carlos Cerqueira Souza Filho",
            "advogados": [
            "Vinicius Faria de Cerqueira"
            ],
        },
        "reu": {
            "nome": "Cony Engenharia Ltda.",
            "advogados": [
                "Carlos Henrique de Mendonça Brandão",
                "Guilherme Freire Furtado",
                "Maria Eugênia Barreiros de Mello",
                "Vítor Reis de Araujo Carvalho",
            ]
        }
    },
    "movimentacoes": [
        {
            "data": "24/08/2023",
            "titulo": "Arquivado Definitivamente",
            "movimento": "Arquivado Definitivamente"
        }
    ]
}

resultado_RasparTjalSegundoGrau = {
    'cnj': '0710802-55.2018.8.02.0001',
    'classe': 'Apelação Cível',
    'area': 'Cível',
    'assunto': 'Obrigações',
    'juiz': 'José Cícero Alves da Silva',
    'valor_da_acao': '281.178,42',
    'partes_do_processo': [{
        'tipo': 'Apelante:',
        'nome': 'Cony Engenharia Ltda.'
    }, {
        'tipo': 'Apelante:',
        'nome': 'Banco do Brasil S A'
    }, {
        'tipo': 'Apelado:',
        'nome': 'José Carlos Cerqueira Souza Filho'
    }, {
        'tipo': 'Apelada:',
        'nome': 'Livia Nascimento da Rocha'
    }],
    'movimentacoes': [{
        'data': '26/04/2023',
        'titulo': 'Certidão de Envio ao 1º Grau',
        'movimento': 'Faço remessa dos presentes autos à Origem.'
    }, {
        'data': '26/04/2023',
        'titulo': 'Baixa Definitiva',
        'movimento': ''
    }, {
        'data': '26/04/2023',
        'titulo': 'Certidão Emitida',
        'movimento': 'TERMO DE BAIXA Faço baixar estes autos ao Exmo(a). Juiz(a) de Direito da 4ª Vara Cível da Capital, em cumprimento ao despacho de página 872. Maceió, 26 de abril de 2023. Eleonora Paes Cerqueira de França Diretora Adjunta Especial de Assuntos Judiciários Cícera Cristina Lima de Araújo Bandeira Analista Judiciário'
    }, {
        'data': '12/04/2023',
        'titulo': 'Publicado',
        'movimento': ''
    }, {
        'data': '12/04/2023',
        'titulo': 'Certidão Emitida',
        'movimento': 'Certifico que foi disponibilizado(a) no Diário da Justiça Eletrônico do Tribunal de Justiça de Alagoas, nesta data, o(a) Despacho/Decisão retro, nos termos do art 4º, § 3º, da Lei nº 11.419/2006. Maceió, 12 de abril de 2023 Eleonora Paes Cerqueira de França Diretora Adjunta Especial de Assuntos Judiciários'
    }]
}

@patch('app.main.RasparTjal', return_value=resultado_RasparTjal)
@patch('app.main.RasparTjalSegundoGrau', return_value=resultado_RasparTjalSegundoGrau)
def test_garante_que_recebemos_todas_informacoes(mocked_RasparTjal, mocked_RasparTjalSegundoGrau):
    resposta = client.post(
        "/buscar",
        json={"cnj": "0710802-55.2018.8.02.0001"},
    )
    
    assert resposta.status_code == 200
    resultado_json = {
        'processo': {
            'primeiro_grau': {
                'cnj': '0710802-55.2018.8.02.0001',
                'classe': 'Procedimento Comum Cível',
                'area': 'Cível',
                'assunto': 'Dano Material',
                'data_de_distribuicao': '02/05/2018',
                'juiz': 'José Cícero Alves da Silva',
                'valor_da_acao': '281.178,42',
                'partes_do_processo': None,
                'movimentacoes': [
                    {'data': '24/08/2023',
                    'titulo': 'Arquivado Definitivamente',
                    'movimento': 'Arquivado Definitivamente'}
                ]
            },
            'segundo_grau': {
                'cnj': '0710802-55.2018.8.02.0001',
                'classe': 'Apelação Cível',
                'area': 'Cível',
                'assunto': 'Obrigações',
                'juiz': 'José Cícero Alves da Silva',
                'valor_da_acao': '281.178,42',
                'partes_do_processo': [
                    {'tipo': 'Apelante:',
                    'nome': 'Cony Engenharia Ltda.'}, {'tipo': 'Apelante:',
                    'nome': 'Banco do Brasil S A'}, {'tipo': 'Apelado:',
                    'nome': 'José Carlos Cerqueira Souza Filho'}, {'tipo': 'Apelada:',
                    'nome': 'Livia Nascimento da Rocha'}
                ],
                'movimentacoes': [{
                    'data': '26/04/2023',
                    'titulo': 'Certidão de Envio ao 1º Grau',
                    'movimento': 'Faço remessa dos presentes autos à Origem.'}, {'data': '26/04/2023',
                    'titulo': 'Baixa Definitiva',
                    'movimento': ''}, {'data': '26/04/2023',
                    'titulo': 'Certidão Emitida',
                    'movimento': 'TERMO DE BAIXA Faço baixar estes autos ao Exmo(a). Juiz(a) de Direito da 4ª Vara Cível da Capital, em cumprimento ao despacho de página 872. Maceió, 26 de abril de 2023. Eleonora Paes Cerqueira de França Diretora Adjunta Especial de Assuntos Judiciários Cícera Cristina Lima de Araújo Bandeira Analista Judiciário'}, {'data': '12/04/2023',
                    'titulo': 'Publicado',
                    'movimento': ''}, {'data': '12/04/2023',
                    'titulo': 'Certidão Emitida',
                    'movimento': 'Certifico que foi disponibilizado(a) no Diário da Justiça Eletrônico do Tribunal de Justiça de Alagoas, nesta data, o(a) Despacho/Decisão retro, nos termos do art 4º, § 3º, da Lei nº 11.419/2006. Maceió, 12 de abril de 2023 Eleonora Paes Cerqueira de França Diretora Adjunta Especial de Assuntos Judiciários'}
                    ]}
                }}
    assert resposta.json() == resultado_json

def test_garante_que_cnj_não_seja_vazio():
    resposta = client.post(
        "/buscar",
        json={"cnj": ""}
    )
    assert resposta.status_code == 400
    assert resposta.json() == {
        "message":"Cnj vazio."
    }