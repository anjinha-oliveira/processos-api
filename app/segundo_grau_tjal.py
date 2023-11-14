from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

import requests
from lxml import etree 

from bs4 import BeautifulSoup


def RasparTjalSegundoGrau(cnj):

    service = Service(ChromeDriverManager().install())

    navegador = webdriver.Chrome(service=service)

    navegador.get("https://www2.tjal.jus.br/cposg5/open.do")
    navegador.find_element("xpath", '//*[@id="radioNumeroAntigo"]').click()
    navegador.find_element("xpath", '//*[@id="nuProcessoAntigoFormatado"]').send_keys('0710802-55.2018.8.02.0001')
    navegador.find_element("xpath", '//*[@id="pbConsultar"]').click()
    navegador.find_element("xpath", '//*[@id="processoSelecionado"]').click()
    navegador.find_element("xpath", '//*[@id="botaoEnviarIncidente"]').click()


    soup = BeautifulSoup(navegador.page_source, "html.parser")
    
    cnj = soup.select("#numeroProcesso")[0].text.strip()
    if not cnj:
        return None
    
    classe = soup.select("#classeProcesso")[0].text.strip()
    area = soup.select("#areaProcesso")[0].text.strip()
    assunto = soup.select("#assuntoProcesso")[0].text.strip()
    orgao_julgador = soup.select("#orgaoJulgadorProcesso")[0].text.strip()
    valor_da_acao = soup.select("#valorAcaoProcesso")[0].text.strip()

    partes_do_processo = []
    #import pdb; pdb.set_trace()
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
    trs = soup.select("#tabelaUltimasMovimentacoes tr")
    for tr in trs:
        data_movimentacao = tr.select(".dataMovimentacaoProcesso")[0].contents[0].strip()
        
        conteudos =  tr.select(".descricaoMovimentacaoProcesso")[0].contents
        if conteudos[0].text.strip():
            titulo_movimentacao = conteudos[0].text.strip()
        else:
            titulo_movimentacao = conteudos[1].text.strip()

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
        "orgao_julgador": orgao_julgador,
        "valor_da_acao": valor_da_acao,
        "partes_do_processo": partes_do_processo,
        "movimentacoes": movimentacoes,
    }


