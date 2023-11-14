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
    navegador.find_element("xpath", '//*[@id="nuProcessoAntigoFormatado"]').send_keys("0070337-91.2008.8.06.0001")
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
    import pdb; pdb.set_trace()
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
        



    return {
        "primeiro_grau": {
            "cnj": cnj,
            "classe": classe,
            "area": area,
            "assunto": assunto,
            "data_de_distribuicao": data_de_distribuicao,
            "juiz": juiz,
            "valor_da_acao": valor_da_acao,
        }
        
    }