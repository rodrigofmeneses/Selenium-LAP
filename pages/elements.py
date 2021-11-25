# from abc import ABC
from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
from page_objects import PageElement


class Login(PageElement):
    login_input = (By.ID, 'user-name')
    password_input = (By.ID, 'password')
    submit_button = (By.CSS_SELECTOR, '[type="submit"]')

    def logar(self, usuario, senha):
        self.find_element(self.login_input).send_keys(usuario)
        self.find_element(self.password_input).send_keys(senha)
        self.find_element(self.submit_button).click()


class Planejamento(PageElement):
    spg_button = (By.CSS_SELECTOR, '.ng-tns-c37-10')

    def acessarSpg(self):
        self.find_element(self.spg_button).click()


class Terceirizados(PageElement):

    loc_funcionarios = (By.CSS_SELECTOR, 'tbody > tr')

    def funcionarios_cadastrados(self):
        funcionarios = self.find_elements(self.loc_funcionarios)

        po_funcionarios = []
        for funcionario in funcionarios:
            po_funcionarios.append(Funcionario(funcionario))

        return po_funcionarios


class DemaisInformacoes(PageElement):
    ...


class Funcionario():
    def __init__(self, selenium_object):
        """
        Funcionario contem as informações do Terceirizados.
        selenium_object: objeto te a linha na tabela a qual
        o funcionario pertence.
        """
        self.selenium_object = selenium_object
        # Informações
        self.nome = (By.CSS_SELECTOR, 'div > span')
        self.cpf = (By.CSS_SELECTOR, 'span > span')
        self.dias_trabalhados = None
        self.salario_base = None
        self.salario_total = None
        # Elementos
        self._dias_trabalhados = self.dias_trabalhados
        self._salario_base = self.salario_base
        self._demais_informacoes = (By.CSS_SELECTOR, 'button')
        self._load()

    def demais_informacoes(self):
        self.selenium_object.find_element(*self._demais_informacoes).click()

    def modificar_dias_trabalhados(self, dias):
        ...

    def modificar_salario_base(self, salario):
        ...

    def _load(self):
        self.nome = self.selenium_object.find_element(
            *self.nome
        ).text

        self.cpf = self.selenium_object.find_element(
            *self.cpf
        ).text

        # inputs
        inputs = (By.CSS_SELECTOR, 'input')

        # dias trabalhados
        input_elements = self.selenium_object.find_elements(
            *inputs
        )

        self.dias_trabalhados = input_elements[0].get_attribute('value')
        self.dias_trabalhados = float(
            self.dias_trabalhados.replace('.', '').replace(',', '.')
        )
        # elemento clicável
        self._dias_trabalhados = input_elements[0]

        # salario base
        self.salario_base = input_elements[1].get_attribute('value')
        self.salario_base = float(
            self.salario_base.replace('.', '').replace(',', '.')
        )
        # elemento clicável
        self._salario_base = input_elements[1]

        # salario total
        self.salario_total = input_elements[7].get_attribute('value')
        self.salario_total = float(
            self.salario_total.replace('.', '').replace(',', '.')
        )

    def __repr__(self):
        return "ALOOOOO"
        # return f'Funcionario(nome="{self.nome}"", cpf="{self.cpf}")'


class SpecialInput():

    def input(elemento, novo_valor):
        ...
