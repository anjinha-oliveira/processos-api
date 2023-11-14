from fastapi import FastAPI
from fastapi.responses import JSONResponse

from raspagem_tjal import RasparTjal
from raspagem_tjce import RasparTjce
from segundo_grau_tjal import RasparTjalSegundoGrau
from segundo_grau_tjce import RasparTjceSegundoGrau

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

    segundo_grau = None
    primeiro_grau = RasparTjal(
        url=f"https://www2.tjal.jus.br/cpopg/show.do?processo.numero={processo.cnj}",
    )
    if primeiro_grau:
        segundo_grau = RasparTjalSegundoGrau(
            processo.cnj
        )
    else:
        primeiro_grau = RasparTjce(
            processo.cnj
        )
        if primeiro_grau:
            segundo_grau = RasparTjceSegundoGrau(processo.cnj)
    

    if not primeiro_grau:
        return JSONResponse(
            content={"message": "Cnj inválido."},
            status_code=400
        )

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
                "partes_do_processo": primeiro_grau.get("partes_do_processo"),
                "movimentacoes": primeiro_grau.get("movimentacoes"),
            },
            "segundo_grau": {
                "cnj": segundo_grau.get("cnj"),
                "classe": segundo_grau.get("classe"),
                "area": segundo_grau.get("area"),
                "assunto": segundo_grau.get("assunto"),
                "juiz": segundo_grau.get("juiz"),    
                "valor_da_acao": segundo_grau.get("valor_da_acao"),
                "partes_do_processo": segundo_grau.get("partes_do_processo"),
                "movimentacoes": segundo_grau.get("movimentacoes")
            }
        }
    }
