import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import PySimpleGUI as sg
from selenium.webdriver.common.action_chains import ActionChains

class mlScrap():
    def __init__(self):
        option = Options()
        option.headless = True

        self.url = 'https://www.mercadolivre.com.br/'
        self.driver = webdriver.Firefox(options=option)

        self.driver.get(url=self.url)

    def pesquisar(self, produto):
        barra_de_pesquisa = self.driver.find_element_by_xpath('//input[@name="as_word"]')
        barra_de_pesquisa.send_keys(produto)

        button_search = self.driver.find_element_by_xpath('//button[@class="nav-search-btn"]')
        button_search.click()
        time.sleep(1.5)

        cookies = self.driver.find_element_by_xpath('//button[@id="cookieDisclaimerButton"]')
        cookies.click()

    def pegarDados(self):
        nomes = self.driver.find_elements_by_xpath('//li[@class="ui-search-layout__item"]//h2[@class="ui-search-item__title ui-search-item__group__element"]')

        precos = self.driver.find_elements_by_xpath('//div[@class="ui-search-price ui-search-price--size-medium ui-search-item__group__element"]//span[@class="price-tag ui-search-price__part"]//span[@class="price-tag-fraction"]')

        links = self.driver.find_elements_by_xpath('//a[@class="ui-search-result__content ui-search-link"]')

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
                i+=1
            except:
                try:
                    self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    proxima_pagina = self.driver.find_element_by_xpath('//li[@class="andes-pagination__button andes-pagination__button--next"]//a[@class="andes-pagination__link ui-search-link"]').get_attribute('href')
                    print(proxima_pagina)
                    self.driver.get(proxima_pagina)
                    time.sleep(1.25)
                    self.pegarDados()
                except:
                    pass

        dados.close()

    def frete_Gratis(self, scrollFrom = 0, scollTo = 1):
        try:
            frete = self.driver.find_element_by_xpath('//*[contains(text(), "Gratis")]')
            frete.click()
            time.sleep(3)
        except:
            sFrom = 0
            sTo = 300
            sFrom += 400
            sTo += 400
            self.frete_Gratis(sFrom, sTo)

    def envio_Full(self, scrollFrom = 0, scollTo = 1):
        try:
            frete_gratis = self.driver.find_element_by_xpath('//*[contains(text(), "Frete grátis")]')
            if frete_gratis:
                full = self.driver.find_element_by_xpath('//span[@class="ui-search-animated-switch__switch-bar ui-search-animated-switch__switch-bar--off"]')
                full.click()
                time.sleep(2)
        except:
            try:
                full = self.driver.find_element_by_xpath('//svg[@class="ui-search-icon ui-search-icon--full ui-search-filter-icon--full"]')
                full.click()
                time.sleep(2)
            except:
                sFrom = 0
                sTo = 300
                sFrom += 400
                sTo += 400
                self.envio_Full(sFrom, sTo)

    def NU(self, scrollFrom = 0, scollTo = 1, old = False):
        try:
            new_ = self.driver.find_element_by_xpath('//*[contains(text(), "Novo")]')
            old_ = self.driver.find_element_by_xpath('//*[contains(text(), "Usado")]')
            if new_ and old_:
                try:
                    try:
                        new = self.driver.find_element_by_xpath('//*[contains(text(), "Novo")]')
                        new.click()
                        time.sleep(5)
                    except:
                        sFrom = 0
                        sTo = 300
                        sFrom += 400
                        sTo += 400
                        self.NU(sFrom, sTo)
                except:
                    pass
            else:
                try:
                    try:
                        old = self.driver.find_element_by_xpath('//*[contains(text(), "Usado")]')
                        old.click()
                        time.sleep(5)
                    except:
                        sFrom = 0
                        sTo = 300
                        sFrom += 400
                        sTo += 400
                        self.NU(sFrom, sTo)
                except:
                    pass
        except:
            pass

    def filtrar(self, min, max='', scrollFrom = 0, scollTo = 1):
        try:
            filtrar_min = self.driver.find_element_by_xpath('//input[@data-testid="Minimum-price"]')
            filtrar_min.click()
            filtrar_min.send_keys(min)

            filtrar_max = self.driver.find_element_by_xpath('//input[@data-testid="Maximum-price"]')
            filtrar_max.click()
            filtrar_max.send_keys(max)

            filtrar_max.send_keys(Keys.RETURN)
            time.sleep(3)
        except:
            sFrom = 0
            sTo = 300
            sFrom += 400
            sTo += 400
            self.filtrar(min, max, scrollFrom=sFrom, scollTo=sTo)

classe = mlScrap()
# Layout
sg.theme('reddit')

layout = [
    [sg.Text('Produto:')], [sg.Input(key='produto', size=(20, 2))],
    [sg.Text('Frete gratis')], [sg.Radio('Sim   ', key='Frete_s', group_id='Frete'), sg.Radio('Não', key='Frete_n', default=True, group_id='Frete')],
    [sg.Text('Envio full')], [sg.Radio('Sim    ', key='Full_s', group_id='Full'), sg.Radio('Não', key='Full_n', default=True, group_id='Full')],
    [sg.Text('Novo/Usado')], [sg.Radio('Novo    ', key='Novo', group_id='NU'), sg.Radio('Usado', key='Usado', group_id='NU')],
    [sg.Text('Filtrar por preços')], [sg.Text('Min: '), sg.Input(key='p_min', size=(10, 2), default_text='0'), sg.Text('Max:  '),sg.Input(key='p_max', size=(10, 2))],
    [sg.Button('Garimpar!')]
]

# Janela
janela = sg.Window('Garimpar ML', layout, element_justification='c')

# eventos
while True:
    eventos, valores = janela.read()

    if eventos == 'Garimpar!':
        classe.pesquisar(valores['produto'])
        if valores['Frete_s']:
            classe.frete_Gratis()
        if valores['Full_s']:
            classe.envio_Full()
        if valores['Novo']:
            classe.NU()
        if valores['Usado']:
            classe.NU(old=True)
        if valores['p_min'] != '0':
            classe.filtrar(valores['p_min'], valores['p_max'])

        classe.pegarDados()