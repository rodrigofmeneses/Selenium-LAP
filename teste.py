from selenium.webdriver import Firefox
# from pages.pages import PageLogin, PageGuardiao, PageSPG, PageFatura
from scripts.inicializar import Inicializar

# Provisórios
from time import sleep
from selenium.webdriver.common.by import By

browser = Firefox()
browser.maximize_window()

pagina = Inicializar(
    browser,
    'https://guardiaov4.seplag.ce.gov.br/auth',
    'credenciais.txt'
).run()
