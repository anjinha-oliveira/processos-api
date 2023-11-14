import requests
from lxml import etree 

from bs4 import BeautifulSoup


def RasparTjal(url):
    response_raw = requests.get(url)
    soup = BeautifulSoup(response_raw.text, "html.parser")

    response = etree.HTML(str(soup))

    if not response.xpath('//*[@id="numeroProcesso"]/text()'):
        return None

    cnj = response.xpath('//*[@id="numeroProcesso"]/text()')[0].strip()
    classe = response.xpath('//*[@id="classeProcesso"]/text()')[0]
    area = response.xpath('//*[@id="areaProcesso"]/span/text()')[0]
    assunto = response.xpath('//*[@id="assuntoProcesso"]/text()')[0]
    data_de_distribuicao = response.xpath(
        '//*[@id="dataHoraDistribuicaoProcesso"]/text()'
    )[0].split()[0]
    juiz = response.xpath('//*[@id="juizProcesso"]/text()')[0]
    valor_da_acao = response.xpath(
        '//*[@id="valorAcaoProcesso"]/text()'
    )[0].replace(' ', '')

    partes_do_processo = []
    trs = soup.select("#tableTodasPartes tr")
    for tr in trs:
        participacao = tr.select(".mensagemExibindo")[0].contents[0].strip()
        nome = tr.select(".nomeParteEAdvogado")[0].contents[0].strip()

        partes_do_processo.append(
            {
                "tipo": participacao,
                "nome": nome,
            }
        )
        
    movimentacoes = []
    trs = soup.select("#tabelaTodasMovimentacoes tr")
    for tr in trs:

        data_movimentacao = tr.select(".dataMovimentacao")[0].contents[0].strip()
        titulo_movimentacao = tr.select(".descricaoMovimentacao")[0].contents[0].strip()
        descricao_movimentacao = tr.select('span')[0].text.strip()

        movimentacoes.append(
            {
                "data": data_movimentacao,
                "titulo": titulo_movimentacao,
                "movimento": descricao_movimentacao,
            }
        )

    return {
        "cnj": cnj,
        "classe": classe,
        "area": area,
        "assunto": assunto,
        "data_de_distribuicao": data_de_distribuicao,
        "juiz": juiz,
        "valor_da_acao": valor_da_acao,
        "partes_do_processo": partes_do_processo,
        "movimentacoes": movimentacoes,
    }

