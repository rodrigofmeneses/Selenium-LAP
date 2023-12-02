from selenium.webdriver import Firefox

# from pages.pages import PageLogin, PageGuardiao, PageSPG, PageFatura
from scripts.inicializar import Inicializar
from scripts.preencher_fatura import PreencherFatura

# Provisórios
from time import sleep
from selenium.webdriver.common.by import By

browser = Firefox()
browser.maximize_window()

pagina = Inicializar(
    browser, "https://guardiaov4.seplag.ce.gov.br/auth", "credenciais.txt"
).run()

p = PreencherFatura(
    browser,
    "data/SSPDS 009 (06-2022).xlsx",
    intervalo_funcionarios=(15, 103),
    nome_planilha="SPG",
)

p.run()
