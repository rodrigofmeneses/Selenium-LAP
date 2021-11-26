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
    _tabela_terceirizados_locator = (By.CSS_SELECTOR, 'tbody > tr')
    funcionarios = []


    def _funcionarios_cadastrados(self):
        num_funcs = len(self.find_elements(self._tabela_terceirizados_locator))
        po_funcs = []
        for n in range(1, num_funcs + 1):
            po_funcs.append(Funcionario(
                self.webdriver,
                (By.CSS_SELECTOR, f'tbody > tr:nth-child({n})')
            ))
        return po_funcs

    def carregar_funcionarios(self):
        self.funcionarios = self._funcionarios_cadastrados()


class ClickAgent():
    def inserir(self, locator, valor):
        # uma grande pegadinha é que esse locator é a partir do elemento
        # e não da página.
        elemento = self.find_element(locator)
        # Se o valor tem uma casa decimal, deve inserir de maneira diferente,
        # com um 0 extra, pois 3.20 se torna 0.32
        if len(str(valor).split('.')[-1]) == 1:
            if valor < 0:
                self._inserir_com_modificador_final(elemento, valor, '0-')
            else:
                self._inserir_com_modificador_final(elemento, valor, '0')
        else:
            if valor < 0:
                self._inserir_com_modificador_final(elemento, valor, '-')
            else:
                self._inserir_com_modificador_final(elemento, valor)

    def _inserir_com_modificador_final(self, elemento, valor, modificador=''):
        elemento.clear()
        elemento.send_keys(
            f"0{str(valor)}{modificador}"
        )

    def clicar(self, locator):
        self.find_element(locator).click()


class Funcionario(PageElement, ClickAgent):
    def __init__(self, webdriver, locator):
        """
        Funcionario contem as informações do Terceirizados.
        selenium_object: objeto te a linha na tabela a qual
        o funcionario pertence.

        Funcionário é dinâmico, sempre que mexer em algo, tem que atualizar.
        """
        self.webdriver = webdriver
        self._locator = locator
        # Informações
        self.nome = (By.CSS_SELECTOR, 'div > span')
        self.cpf = (By.CSS_SELECTOR, 'span > span')
        self.dias_trabalhados = (By.CSS_SELECTOR, 'td:nth-child(6) input')
        self.salario_base = (By.CSS_SELECTOR, 'td:nth-child(7) input')
        self.salario_total = (By.CSS_SELECTOR, 'td:nth-child(13) input')
        # Seletores
        self._nome = self.nome
        self._cpf = self.cpf
        self._dias_trabalhados = self.dias_trabalhados
        self._salario_base = self.salario_base
        self._salario_total = self.salario_total
        self._demais_informacoes = (By.CSS_SELECTOR, 'button')
        # Atualizar o webdriver para o elemento
        self.webdriver = self.find_element(
            self._locator
        )
        self._load()

    def modificar_dias_trabalhados(self, valor):
        modificar(self._dias_trabalhados, valor)

    def modificar_salario_base(self, valor):
        modificar(self._salario_base, valor)

    def modificar(self, locator, valor):
        self.inserir(locator, valor)
        self.clicar(self._nome)
        sleep(3)
        self._load()

    def demais_informacoes(self):
        self.find_element(self._demais_informacoes).click()
        return DemaisInformacoes(self.webdriver, self.cpf)

    def _load(self):
        self.nome = self._load_text(self._nome)
        self.cpf = self._load_text(self._cpf)
        self.dias_trabalhados = self._load_atrib_value(self._dias_trabalhados)
        self.salario_base = self._load_atrib_value(self._salario_base)
        self.salario_total = self._load_atrib_value(self._salario_total)

    def _load_text(self, locator):
        return self.find_element(locator).text

    def _load_atrib_value(self, locator):
        text = self.find_element(locator).get_attribute('value')
        return float(text.replace('.', '').replace(',', '.'))

    def __repr__(self):
        return f'Funcionario(nome="{self.nome}"", cpf="{self.cpf}")'

class DemaisInformacoes(PageElement, ClickAgent):
    def __init__(self, webdriver, cpf):
        self.webdriver = webdriver
        self.cpf = cpf
        self.montanteA = (By.CSS_SELECTOR, '')
        self.montanteB = (By.CSS_SELECTOR, '')
        self.montanteC = (By.CSS_SELECTOR, '')
        self.provisionamento = (By.CSS_SELECTOR, '')

    def preencher_montante_A():
        ...

    def preencher_montante_B():
        ...

    def preencher_montante_C():
        ...

    def preencher_provisionamento():
        ...
