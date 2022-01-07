from selenium.webdriver import Firefox
from pages.pages import PageLogin
from time import sleep

class TestClassLogin:
    pagina = PageLogin(Firefox(), 'https://guardiaov4.seplag.ce.gov.br/auth') 
    pagina.open()

    def test_quando_acessar_a_pagina_de_login_entao_deve_retornar_o_titulo(self):
        assert self.pagina.webdriver.title == 'Guardião - Sistema de Controle de Acesso'
    
    def test_quando_acessar_o_elemento_login_entao_deve_retornar_seu_id_user_name(self):
        login_id = self.pagina.find_element(self.pagina.login._loc_login).get_attribute('id')
        assert login_id == 'user-name', 'O locator do login foi alterado'

    def test_quando_acessar_o_elemento_password_entao_deve_retornar_seu_id_password(self):
        password_id = self.pagina.find_element(self.pagina.login._loc_password).get_attribute('id')
        assert password_id == 'password', 'O locator do password foi alterado'
    
    def test_quando_acessar_o_elemento_submit_entao_deve_retornar_seu_type_submit(self):
        submit_type = self.pagina.find_element(self.pagina.login._loc_submit).get_attribute('type')
        assert submit_type == 'submit', 'O locator do submit foi alterado'
    
    def test_quando_ler_credenciais_deve_retornar_usuario_diferente_de_nulo(self):
        self.pagina.login.ler_credenciais('credenciais.txt')
        assert self.pagina.login.usuario != '', 'As credenciais estão vazias'

    def test_quando_ler_credenciais_deve_retornar_senha_diferente_de_nulo(self):
        self.pagina.login.ler_credenciais('credenciais.txt')
        assert self.pagina.login.senha != '', 'As credenciais estão vazias'

    def test_quando_logar_deve_mudar_de_pagina(self):
        url_antiga = self.pagina.webdriver.current_url
        self.pagina.login.logar('credenciais.txt')
        sleep(2)
        assert self.pagina.webdriver.current_url != url_antiga, 'Não foi possível logar'
    
    def test_quando_logar_a_pagina_deve_ser_a_home(self):
        assert self.pagina.webdriver.current_url == 'https://guardiaov4.seplag.ce.gov.br/home'
        self.pagina.webdriver.close()