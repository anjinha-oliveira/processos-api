from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

import requests
from lxml import etree 

from bs4 import BeautifulSoup


def RasparTjce(cnj):
    service = Service(ChromeDriverManager().install())

    navegador = webdriver.Chrome(service=service)


    navegador.get("https://esaj.tjce.jus.br/cpopg/open.do")
    navegador.find_element("xpath", '//*[@id="radioNumeroAntigo"]').click()
    navegador.find_element("xpath", '//*[@id="nuProcessoAntigoFormatado"]').send_keys(cnj)
    navegador.find_element("xpath", '//*[@id="botaoConsultarProcessos"]').click()
    

    soup = BeautifulSoup(navegador.page_source, "html.parser")
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
    juiz = ''
    if response.xpath('//*[@id="juizProcesso"]/text()'):
        juiz = response.xpath(
            '//*[@id="juizProcesso"]/text()'
        )[0].replace(' ', '')
    valor_da_acao = ''
    if response.xpath('//*[@id="valorAcaoProcesso"]/text()'):
        valor_da_acao = response.xpath(
            '//*[@id="valorAcaoProcesso"]/text()'
        )[0].replace(' ', '')

    partes_do_processo = []
    trs = soup.select("#tablePartesPrincipais tr")
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
    trs = soup.select("#tabelaUltimasMovimentacoes tr")
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
        "movimentacoes": movimentacoes
    }