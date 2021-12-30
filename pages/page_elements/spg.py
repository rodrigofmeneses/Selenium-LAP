from page_objects import PageElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from time import sleep


class MenuSuperior(PageElement):
    sister_button = (By.CSS_SELECTOR, 'li:nth-child(6) > a.menu')
    
    def clicar_sister(self):
        try:
            botao = WebDriverWait(self.webdriver, 10).until(
                expected_conditions.presence_of_element_located(
                    self.sister_button
                )
            )
        finally:
            sleep(1)
            self._clicar(self.sister_button)


class MenuLateral(PageElement):
    fatura_button = (
        By.CSS_SELECTOR, 
        'ul:nth-child(1) > li:nth-child(7) > a:nth-child(1)'
    )
    controle_de_fatura_button = (
        By.CSS_SELECTOR, 
        'li.active:nth-child(7) > ul:nth-child(2) > li:nth-child(1) > a:nth-child(1)'
    )

    def clicar_fatura(self):
        self._clicar(self.fatura_button)
    
    def clicar_controle_de_fatura(self):
        self._clicar(self.controle_de_fatura_button)


class Avisos(PageElement):
    close_button = (By.CSS_SELECTOR, 'button.close')

    def fechar_avisos(self):
        sleep(2)
        num_avisos = len(self.find_elements(self.close_button))
        for _ in range(num_avisos):
            for button in self.find_elements(self.close_button):
                try: 
                    button.click()
                except:
                    ...
            sleep(0.2)
        sleep(1)