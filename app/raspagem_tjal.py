
import requests
from lxml import etree 

from bs4 import BeautifulSoup

def RasparTjal(cnj):

    URL = f"https://www2.tjal.jus.br/cpopg/show.do?processo.numero={cnj}"
    response_raw = requests.get(URL)
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
    autor = soup.select(
        "#tablePartesPrincipais .nomeParteEAdvogado"
    )[0].contents[0].replace('\t', '').replace('\n', '')
    autor_adv = soup.select(
        "#tablePartesPrincipais .nomeParteEAdvogado"
    )[0].contents[4].replace('\t', '').replace('\n', '')

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
        "data_de_distribuicao": data_de_distribuicao,
        "juiz": juiz,
        "valor_da_acao": valor_da_acao,
        "autor": autor,
        "autor_adv": autor_adv,
    }

