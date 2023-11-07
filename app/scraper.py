import scrapy


class BrickSetSpider(scrapy.Spider):
    name = "consltar_por_cnj"
    start_urls = ['https://www2.tjal.jus.br/cpopg/open.do']

    def parse(self, response):
        cb_pesquisa = response.xpath('//*[@id="cbPesquisa"]/option[1]')
        cb_pesquisa_text = cb_pesquisa.get()
        self.log(cb_pesquisa_text)


class InfosProcesso(scrapy.Spider):
    name = "resultado_cnj"
    start_urls = [
        'https://www2.tjal.jus.br/cpopg/show.do?processo.codigo=01000O7550000&processo.foro=1&processo.numero=0710802-55.2018.8.02.0001'
    ]

    def parse(self, response):
        cnj = response.xpath('//*[@id="numeroProcesso"]/text()').get().strip()
        classe = response.xpath('//*[@id="classeProcesso"]/text()').get()
        area = response.xpath('//*[@id="areaProcesso"]/span/text()').get()
        assunto = response.xpath('//*[@id="assuntoProcesso"]/text()').get()
        data_de_distribuicao = response.xpath(
            '//*[@id="dataHoraDistribuicaoProcesso"]/text()'
        ).get().split()[0]
        juiz = response.xpath('//*[@id="juizProcesso"]/text()').get()
        valor_da_acao = response.xpath(
            '//*[@id="valorAcaoProcesso"]/text()'
        ).get().replace(' ', '')
        autor, adv_autor = response.xpath(
            '//*[@id="tablePartesPrincipais"]/tr[1]/td[2]'
        ).get().replace('\n', '').replace('\t', '').split('<br>')