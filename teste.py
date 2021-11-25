from selenium.webdriver import Firefox
from pages.pages import PageLogin, PageGuardiao, PageFatura

# Provisórios
from time import sleep
from selenium.webdriver.common.by import By
from pages.elements import Funcionario


with open('credenciais.txt') as f:
    login = f.readline()
    senha = f.readline()

browser = Firefox()

pagina = PageLogin(
    browser,
    'https://guardiaov4.seplag.ce.gov.br/auth'
)

pagina.open()
pagina.login.logar(login, senha)

pagina = PageGuardiao(browser)
sleep(1)
pagina.planejamento.acessarSpg()

pagina = PageFatura(browser)
