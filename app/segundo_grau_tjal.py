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

    apelante = soup.select(
                    "#tableTodasPartes .nomeParteEAdvogado"
                )[0].contents[0].replace("\n", "").replace("\t", "").strip()
    apelante_adv = [
        soup.select(
            "#tableTodasPartes .nomeParteEAdvogado"
        )[0].contents[3].replace('\n', '').replace('\t', '').strip(),
        soup.select(
            "#tableTodasPartes .nomeParteEAdvogado"
        )[0].contents[8].replace('\n', '').replace('\t', '').strip(),
        soup.select(
            "#tableTodasPartes .nomeParteEAdvogado"
        )[0].contents[13].replace('\n', '').replace('\t', '').strip(),
        soup.select(
            "#tableTodasPartes .nomeParteEAdvogado"
        )[0].contents[18].replace('\n', '').replace('\t', '').strip()
    ]
    apelante = soup.select(
        "#tableTodasPartes .nomeParteEAdvogado"
    )[1].contents[0].replace('\n', '').replace('\t', '').strip()
    apelante_adv = [
        soup.select(
            "#tableTodasPartes .nomeParteEAdvogado"
        )[1].contents[3].replace('\n', '').replace('\t', '').strip(),
    ]
    apelado = soup.select(
        "#tableTodasPartes .nomeParteEAdvogado"
    )[2].contents[0].replace('\n', '').replace('\t', '').strip()
    apelado_adv = [
        soup.select(
            "#tableTodasPartes .nomeParteEAdvogado"
        )[2].contents[3].replace('\n', '').replace('\t', '').strip(),
    ]
    apelada = soup.select(
                "#tableTodasPartes .nomeParteEAdvogado"
            )[3].contents[0].replace('\n', '').replace('\t', '').strip(),
    apelada_adv = [
        soup.select(
            "#tableTodasPartes .nomeParteEAdvogado"
        )[3].contents[3].replace('\n', '').replace('\t', '').strip()
    ]
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
        "apelante": apelante,
        "apelante_adv": apelante_adv,
        "apelado": apelado,
        "apelado_adv": apelado_adv,
        "apelada": apelada,
        "apelada_adv": apelada_adv,
        "movimentacoes": movimentacoes,
    }


