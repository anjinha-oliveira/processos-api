from fastapi import FastAPI
from fastapi.responses import JSONResponse

from pydantic import BaseModel

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

    return {
        "processo": {
            "cnj": processo.cnj,
            "classe": "Procedimento Comum Cível",
            "area": "Civíl",
            "assunto": "dano moral",
            "data-distribuicao": "02/05/2018",
            "juiz": "José Cícero Alves da Silva",
            "valor-da-acao": "281.178,42",
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
                    "movimento": "Arquivado Definitivamente"
                }
            ]
        }
    }
