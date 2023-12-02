from page_objects import PageElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


class Planejamento(PageElement):
    spg_button = (By.ID, "glo-elementblock-0")

    def acessar_spg(self):
        try:
            botao = WebDriverWait(self.webdriver, 10).until(
                expected_conditions.presence_of_element_located(
                    self.spg_button
                )
            )
        finally:
            self._clicar(self.spg_button)
