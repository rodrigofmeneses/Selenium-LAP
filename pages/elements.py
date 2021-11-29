# from abc import ABC
from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
from page_objects import PageElement
from time import sleep


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
    loc_tabela_terceirizados = (By.CSS_SELECTOR, 'tbody > tr')
    funcionarios = []


    def _funcionarios_cadastrados(self):
        num_funcs = len(self.find_elements(self.loc_tabela_terceirizados))
        po_funcs = []
        loc_funcionario = 'tbody > tr:nth-child({})'
        for i in range(1, num_funcs + 1):
            po_funcs.append(Funcionario(
                self.webdriver,
                (By.CSS_SELECTOR, loc_funcionario.format(i))
            ))
        return po_funcs

    def carregar_funcionarios(self):
        self.funcionarios = self._funcionarios_cadastrados()


class ClickAgent():
    def _digitar(self, locator, valor):
        # uma grande pegadinha é que esse locator é a partir do elemento
        # e não da página.
        elemento = self.find_element(locator)
        # Se o valor tem uma casa decimal, deve digitar de maneira diferente,
        # com um 0 extra, pois 3.20 se torna 0.32
        if len(str(valor).split('.')[-1]) == 1:
            if valor < 0:
                self._digitar_com_modificador_final(elemento, valor, '0-')
            else:
                self._digitar_com_modificador_final(elemento, valor, '0')
        else:
            if valor < 0:
                self._digitar_com_modificador_final(elemento, valor, '-')
            else:
                self._digitar_com_modificador_final(elemento, valor)

    def _digitar_com_modificador_final(self, elemento, valor, modificador=''):
        elemento.clear()
        elemento.send_keys(
            f"0{str(valor)}{modificador}"
        )

    def _clicar(self, locator):
        self.find_element(locator).click()


class Funcionario(PageElement, ClickAgent):
    def __init__(self, webdriver, loc_funcionario):
        """
        Funcionario contem as informações do Terceirizados.
        selenium_object: objeto te a linha na tabela a qual
        o funcionario pertence.

        Funcionário é dinâmico, sempre que mexer em algo, tem que atualizar.
        """
        self.webdriver = webdriver
        # Informações
        self.nome = (By.CSS_SELECTOR, loc_funcionario[1] + ' ' + 'div > span')
        self.cpf = (By.CSS_SELECTOR, loc_funcionario[1] + ' ' + 'span > span')
        self.dias_trabalhados = (
            By.CSS_SELECTOR,
            loc_funcionario[1] + ' ' + 'td:nth-child(6) input'
        )
        self.salario_base = (
            By.CSS_SELECTOR,
            loc_funcionario[1] + ' ' + 'td:nth-child(7) input'
        )
        self.salario_total = (
            By.CSS_SELECTOR,
            loc_funcionario[1] + ' ' + 'td:nth-child(13) input'
        )
        self.demais_informacoes = (
            By.CSS_SELECTOR,
            loc_funcionario[1] + ' ' + 'button'
        )
        # Seletores
        self.loc_funcionario = loc_funcionario
        self.loc_nome = self.nome
        self.loc_cpf = self.cpf
        self.loc_dias_trabalhados = self.dias_trabalhados
        self.loc_salario_base = self.salario_base
        self.loc_salario_total = self.salario_total
        self.loc_demais_informacoes = self.demais_informacoes

        self._load()

    def modificar_dias_trabalhados(self, valor):
        self._modificar(self.loc_dias_trabalhados, valor)

    def modificar_salario_base(self, valor):
        self._modificar(self.loc_salario_base, valor)

    def _modificar(self, locator, valor):
        self._digitar(locator, valor)
        self._clicar(self.loc_nome)
        # Logo logo botar um wait aqui!
        sleep(3)
        self._load()

    def clicar_demais_informacoes(self):
        self.find_element(self.loc_demais_informacoes).click()
        self.demais_informacoes = DemaisInformacoes(self.webdriver)

    def _load(self):
        self.nome = self._load_text(self.loc_nome)
        self.cpf = self._load_text(self.loc_cpf)
        self.dias_trabalhados = self._load_atrib_value(self.loc_dias_trabalhados)
        self.salario_base = self._load_atrib_value(self.loc_salario_base)
        self.salario_total = self._load_atrib_value(self.loc_salario_total)

    def _load_text(self, locator):
        return self.find_element(locator).text

    def _load_atrib_value(self, locator):
        text = self.find_element(locator).get_attribute('value')
        return float(text.replace('.', '').replace(',', '.'))

    def __repr__(self):
        return f'Funcionario(nome="{self.nome}", cpf="{self.cpf}")'


class DemaisInformacoes(PageElement, ClickAgent):
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.loc_montanteA = (By.CSS_SELECTOR, 'tab.tab-pane:nth-child(1) tbody')
        self.loc_montanteB = (By.CSS_SELECTOR, 'tab.tab-pane:nth-child(2) tbody')
        self.loc_montanteC = (By.CSS_SELECTOR, 'tab.tab-pane:nth-child(3) tbody')
        self.loc_provisionamento_hora_extra = (
            By.CSS_SELECTOR,
            'tab.tab-pane:nth-child(4) > table:nth-child(1) > tbody'
        )
        self.loc_provisionamento_viagem = (
            By.CSS_SELECTOR,
            'tab.tab-pane:nth-child(4) > table:nth-child(2) > tbody'
        )

    def preencher_montante_A(self, dados):
        self._preencher(self.loc_montanteA, dados)
    
    def preencher_montante_B(self, dados):
        self._preencher(self.loc_montanteB, dados)

    def preencher_montante_C(self, dados):
        self._preencher(self.loc_montanteC, dados)
    
    def preencher_provisionamento_hora_extra(self, dados):
        self._preencher(self.loc_provisionamento_hora_extra, dados)

    def preencher_provisionamento_viagem(self, dados):
        self._preencher(self.loc_provisionamento_viagem, dados)

    def _preencher(self, loc_tabela, dados):
        loc_inputs = self._listar_loc_inputs(loc_tabela)
        for loc_input, value in zip(loc_inputs, dados):
            self._digitar(loc_input, value)

    def _listar_loc_inputs(self, loc_tabela):
        complemento = ' ' + 'input'
        num_inputs = len(self.find_elements(
            (loc_tabela[0], loc_tabela[1] + complemento)
        ))
        complemento = ' ' + '> tr:nth-child({}) input'
        loc_inputs = []
        for i in range(1, num_inputs + 1):
            loc_input = (loc_tabela[0], loc_tabela[1] + complemento.format(i))
            if self._input_modificavel(loc_input):
                loc_inputs.append(loc_input)
        return loc_inputs

    def _input_modificavel(self, locator):
        return not bool(self.find_element(locator).get_attribute('readonly'))
