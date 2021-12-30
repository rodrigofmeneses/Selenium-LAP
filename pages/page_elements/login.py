from page_objects import PageElement
from selenium.webdriver.common.by import By

class Login(PageElement):
    _loc_login = (By.ID, 'user-name')
    _loc_password = (By.ID, 'password')
    _loc_submit = (By.CSS_SELECTOR, '[type="submit"]')

    def logar(self, credenciais):
        self.ler_credenciais(credenciais)
        self.find_element(self._loc_login).send_keys(self.usuario)
        self.find_element(self._loc_password).send_keys(self.senha)
        self._clicar(self._loc_submit)
    
    def ler_credenciais(self, credenciais):
        with open(credenciais) as f:
            self.usuario = f.readline()
            self.senha = f.readline()