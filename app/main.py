from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.raspagem_tjal import RasparTjal
from app.raspagem_tjce import RasparTjce

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
    
    dados = RasparTjal(cnj=processo.cnj)

    if not dados:
        return JSONResponse(
            content={"message": "Cnj inválido."},
            status_code=400
        )

    return {
        "processo": {
            "cnj": dados.get("cnj"),
            "classe": dados.get("classe"),
            "area": dados.get("area"),
            "assunto": dados.get("assunto"),
            "data_de_distribuicao": dados.get("data_de_distribuicao"),
            "juiz": dados.get("juiz"),
            "valor_da_acao": dados.get("valor_da_acao"),
            "partes-do-processo": {
                "autor": {
                    "nome": dados.get("autor"),
                    "advogados": [
                        dados.get("autor_adv")
                    ],
                },
                "re": {
                    "nome": dados.get("re"),
                    "advogados": dados.get("re_adv"),
                },
                "reu": {
                    "nome": dados.get("reu"),
                    "advogados": dados.get("reu_adv")
                },
            },
            "movimentacoes": dados.get("movimentacoes")
        },
    }
