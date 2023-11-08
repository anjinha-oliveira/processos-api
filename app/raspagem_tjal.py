
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
    )[0].contents[0].replace('\t', '').replace('\n', '').strip()
    autor_adv = soup.select(
        "#tablePartesPrincipais .nomeParteEAdvogado"
    )[0].contents[4].replace('\t', '').replace('\n', '').strip()
    re = soup.select(
        "#tablePartesPrincipais .nomeParteEAdvogado"
    )[1].contents[0].replace('\n', '').replace('\t', '').strip()
    re_adv = [
        soup.select(
            "#tablePartesPrincipais .nomeParteEAdvogado"
        )[1].contents[4].replace('\n', '').replace('\t', '').strip(),
        soup.select(
            "#tablePartesPrincipais .nomeParteEAdvogado"
        )[1].contents[8].replace('\n', '').replace('\t', '').strip(),
        soup.select(
            "#tablePartesPrincipais .nomeParteEAdvogado"
        )[1].contents[12].replace('\n', '').replace('\t', '').strip()
    ]
    reu = soup.select(
        "#tableTodasPartes .nomeParteEAdvogado"
    )[3].contents[0].replace('\n', '').replace('\t', '').strip()


    reu_adv = {
        soup.select(
            "#tableTodasPartes .nomeParteEAdvogado"
        )[3].contents[4].replace('\n', '').replace('\t', '').strip()
    }
        
    


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
        "re": re,
        "re_adv": re_adv,
        "reu": reu,
        "reu_adv": reu_adv,
    }

