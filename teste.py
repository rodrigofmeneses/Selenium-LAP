from selenium.webdriver import Firefox
from pages.pages import (PageLogin, PageGuardiao, PageSPG, PageFatura)

# Provisórios
from time import sleep
from selenium.webdriver.common.by import By


with open('credenciais.txt') as f:
    login = f.readline()
    senha = f.readline()

browser = Firefox()
browser.maximize_window()

pagina = PageLogin(
    browser,
    'https://guardiaov4.seplag.ce.gov.br/auth'
)
pagina.open()

pagina.login.logar(login, senha)

pagina = PageGuardiao(browser)
pagina.planejamento.acessarSpg()

pagina = PageSPG(browser)
pagina.menu_superior.clicar_sister()

pagina.avisos.fechar_avisos()


pagina.menu_lateral.clicar_fatura()
pagina.menu_lateral.clicar_controle_de_fatura()

pagina = PageFatura(browser)