import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

class olxScrap():
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.url = 'https://www.olx.com.br/'

        self.driver.get(self.url)
        time.sleep(2)

    def pesquisar(self, produto, filtro='sp'):
        barra_de_pesquisa = self.driver.find_element_by_xpath('//input[@id="searchtext"]')
        barra_de_pesquisa.click()
        barra_de_pesquisa.send_keys(produto, Keys.RETURN)
        time.sleep(4)

        # Filtro região
        try:
            if filtro == 'br':
                botao_br = self.driver.find_element_by_xpath('//a[@class="wodqy3-1 kPYWgP sc-jAaTju dlGmlk"]')
                botao_br.click()

            if filtro == 'santos':
                botao_santos = self.driver.find_element_by_xpath('//*[contains(text(), "DDD 13 - Baixada Santista e Litoral Sul")]')
                botao_santos.click()
        except:
            pass

        time.sleep(1.2)

    def pegarDados(self, scrollFrom = 0, scollTo = 1):

        nomes = self.driver.find_elements_by_xpath('//h2[@class="sc-1mbetcw-0 eJfLou sc-ifAKCX jyXVpA"]')

        precos = self.driver.find_elements_by_xpath('//div[@class="aoie8y-0 hRScWw"]//span[@class="sc-ifAKCX eoKYee"]')

        links = self.driver.find_elements_by_xpath('//a[@class="fnmrjs-0 fyjObc"]')

        lista_nomes = []
        lista_precos = []
        lista_links = []

        for nome in nomes:
            lista_nomes.append(nome.text)

        for preco in precos:
            lista_precos.append(preco.text)

        for link in links:
            lista_links.append(link.get_attribute('href'))

        i = 0
        while i <= len(lista_precos):
            try:
                dados = open('produtos.csv', 'a')
                lista_dados = [lista_nomes[i], lista_precos[i], lista_links[i]]
                dados.write(','.join(lista_dados) + '\n')
                print(lista_dados)
                i += 1
            except:
                try:
                    proxima_pagina = self.driver.find_element_by_xpath('//*[contains(text(), "Próxima pagina")]')
                    proxima_pagina.click()
                    if not proxima_pagina:
                        self.driver.execute_script('window.scrollTo(0, 600);')
                        olx_pay = self.driver.find_element_by_xpath('//button[@class="zi8mbi-1 jNFxaY sc-1rn8ww3-0 dJPinE sc-kGXeez cVvyrS"]')
                        olx_pay.click()
                        self.pegarDados()
                    print(proxima_pagina.get_attribute('href'))
                    time.sleep(1.25)
                    self.pegarDados()
                except:
                    sFrom = 0
                    sTo = 300
                    sFrom += 400
                    sTo += 400
                    self.pegarDados(sFrom, sTo)


        dados.close()



classe = olxScrap()
classe.pesquisar('nintendo ds', 'santos')
classe.pegarDados()