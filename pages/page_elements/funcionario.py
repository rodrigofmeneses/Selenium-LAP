from pages.page_elements.type import TypeAgent
from selenium.webdriver.common.by import By


class Funcionario(TypeAgent):
    def __init__(self, webdriver, _loc_funcionario):
        """Funcionario contém todas as informações dos terceirizados."""
        self.webdriver = webdriver
        # Informações
        self.nome = None
        self.cpf = None

        # Seletores
        self._loc_funcionario = _loc_funcionario
        self._loc_nome = (By.CSS_SELECTOR, _loc_funcionario[1] + " div > span")
        self._loc_cpf = (By.CSS_SELECTOR, _loc_funcionario[1] + " span > span")
        self._load_id()

    def _load_id(self):
        self.nome = self._load_text(self._loc_nome)
        self.cpf = self._load_text(self._loc_cpf)

    def _load_data(self):
        ...

    def __repr__(self):
        return f'Funcionario(nome="{self.nome}", cpf="{self.cpf}")'
