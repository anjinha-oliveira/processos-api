from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.raspagem_tjal import RasparTjal
from app.raspagem_tjce import RasparTjce

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from pydantic import BaseModel

service = Service(ChromeDriverManager().install())

app = FastAPI()


class Processo(BaseModel):
    cnj: str


@app.post("/buscar")
async def buscar(processo: Processo):
    if processo.cnj == "":
        return JSONResponse(
            content={"message": "Cnj vazio."},
            status_code=400
        )

    dados = RasparTjal(
        url=f"https://www2.tjal.jus.br/cpopg/show.do?processo.numero={processo.cnj}",
        url_segundo_grau= webdriver.Chrome()"https://www2.tjal.jus.br/cposg5/show.do?processo.codigo=P00006BXP0000"
    )

    # if dados is None:
    #     dados = RasparTjce(
    #         url=f"https://esaj.tjce.jus.br/cpopg/show.do?processo.numero={processo.cnj}"
    #     )
    if not dados:
        return JSONResponse(
            content={"message": "Cnj inválido."},
            status_code=400
        )

    primeiro_grau = dados.get("primeiro_grau")
    return {
        "processo": {
            "primeiro_grau": {
                "cnj": primeiro_grau.get("cnj"),
                "classe": primeiro_grau.get("classe"),
                "area": primeiro_grau.get("area"),
                "assunto": primeiro_grau.get("assunto"),
                "data_de_distribuicao": primeiro_grau.get("data_de_distribuicao"),
                "juiz": primeiro_grau.get("juiz"),
                "valor_da_acao": primeiro_grau.get("valor_da_acao"),
                "partes-do-processo": {
                    "autor": {
                        "nome": primeiro_grau.get("autor"),
                        "advogados": [
                            primeiro_grau.get("autor_adv")
                        ],
                    },
                    "re": {
                        "nome": primeiro_grau.get("re"),
                        "advogados": primeiro_grau.get("re_adv"),
                    },
                    "reu": {
                        "nome": primeiro_grau.get("reu"),
                        "advogados": primeiro_grau.get("reu_adv")
                    },
                },
                "movimentacoes": primeiro_grau.get("movimentacoes")
            },
            "segundo_grau": {
                "cnj": "0710802-55.2018.8.02.0001",
                "classe": "Apelação Cível",
                "area": "Civíl",
                "assunto": "Obrigações",
                "orgao_julgador": "Vice-Presidência",    
                "valor_da_acao": "281.178,42",
                "partes_do_processo": {
                    "apelante": {
                        "nome": "Cony Engenharia Ltda",
                        "advogados": [
                            "Carlos Henrique de Mendonça Brandão"
                        ]
                    },
                    "apelado": {
                        "nome": "José Carlos Cerqueira Souza Filho",
                        "advogados": [
                        "   Vinicius Faria de Cerqueira"
                        ]
                    }
                },
                "movimentacoes": [
                {
                    "data": "26/04/2023",
                    "titulo": "Certidão de Envio ao 1º Grau",
                    "movimento": "Faço remessa dos presentes autos à Origem."
                }
            ]
            }
        }
    }
