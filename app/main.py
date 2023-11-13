from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.raspagem_tjal import RasparTjal
from app.segundo_grau_tjal import RasparTjalSegundoGrau

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

    dados = RasparTjal(
        url=f"https://www2.tjal.jus.br/cpopg/show.do?processo.numero={processo.cnj}",
    )

    segundo_grau = RasparTjalSegundoGrau(
        processo.cnj
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
                "cnj": segundo_grau.get("cnj"),
                "classe": segundo_grau.get("classe"),
                "area": segundo_grau.get("area"),
                "assunto": segundo_grau.get("assunto"),
                "orgao_julgador": segundo_grau.get("orgao_julgador"),    
                "valor_da_acao": segundo_grau.get("valor_da_acao"),
                "partes_do_processo": {
                    "apelante": {
                        "nome": segundo_grau.get("apelante"),
                        "advogados": [
                            segundo_grau.get("apelante_adv"),
                        ]
                    },
                    "apelado": {
                        "nome": segundo_grau.get("apelado"),
                        "advogados": [
                            segundo_grau.get("apelado_adv"),
                        ]
                    },
                    "apelada": {
                        "nome": segundo_grau.get("apelada"),
                        "advogados": [
                            segundo_grau.get("apelada_adv"),
                        ]
                    }
                },
                "movimentacoes": segundo_grau.get("movimentacoes")
            }
        }
    }
