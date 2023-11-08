from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.raspagem_tjal import RasparTjal

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
    
    dados = RasparTjal()

    return {
        "processo": {
            "cnj": dados.get("cnj"),
            "classe": dados.get("classe"),
            "area": dados.get("area"),
            "assunto": dados.get("assunto"),
            "data_de_distribuicao": dados.get("data_de_distribuicao"),
            "juiz": dados.get("juiz"),
            "valor_da_acao": dados.get("valor_da_acao"),
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
                    #  "movimento": "Arquivado Definitivamente"
                # }
            # ]
        }
    }
