
import requests
from lxml import etree 

from bs4 import BeautifulSoup

def RasparTjal():

    URL = 'https://www2.tjal.jus.br/cpopg/show.do?processo.codigo=01000O7550000&processo.foro=1&processo.numero=0710802-55.2018.8.02.0001'
    response_raw = requests.get(URL)
    soup = BeautifulSoup(response_raw.text, "html.parser") 

    response = etree.HTML(str(soup)) 

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

    # Isso aqui precisa ser corrigido e pegar esses dados da página
    # autor, adv_autor = response.xpath(
        # '//*[@id="tablePartesPrincipais"]/tr[1]/td[2]'
    # )[0].text.replace('\n', '').replace('\t', '').split('<br>')

    # autor_tratamento = BeautifulSoup(autor, "html.parser")
    # autor_tratado = autor_tratamento.get_text()

    # adv_autor_tratamento = BeautifulSoup(adv_autor, "html.parser")
    # adv_autor_tratado = adv_autor_tratamento.get_text()

    return {
        "cnj": cnj,
        "classe": classe,
        "area": area,
        "assunto": assunto,
        "data_distribuicao": data_de_distribuicao,
        "juiz": juiz,
        "valor_da_acao": valor_da_acao,
    }
        


