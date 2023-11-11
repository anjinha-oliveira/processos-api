from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())

navegador = webdriver.Chrome(service=service)

navegador.get("https://www2.tjal.jus.br/cposg5/open.do")
navegador.find_element("xpath", '//*[@id="radioNumeroAntigo"]').click()
navegador.find_element("xpath", '//*[@id="nuProcessoAntigoFormatado"]').send_keys('0710802-55.2018.8.02.0001')
navegador.find_element("xpath", '//*[@id="pbConsultar"]').click()
navegador.find_element("xpath", '//*[@id="processoSelecionado"]').click()
navegador.find_element("xpath", '//*[@id="botaoEnviarIncidente"]').click()

import pdb; pdb.set_trace()
