from logging import exception
from pages.page_elements.funcionario import Funcionario
from pages.page_elements.type import TypeAgent
from page_objects import PageElement
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from time import sleep

class TerceirizadosFatura(PageElement):
    _loc_tabela_terceirizados = (By.CSS_SELECTOR, 'tbody > tr')
    funcionarios = []

    def carregar_funcionarios(self):
        self.funcionarios = self._listar_funcionarios_cadastrados()

    def _listar_funcionarios_cadastrados(self):
        num_funcs = len(self.find_elements(self._loc_tabela_terceirizados))
        funcs = []
        _loc_funcionario = 'tbody > tr:nth-child({})'
        for i in range(1, num_funcs + 1):
            funcs.append(FuncionarioFatura(
                self.webdriver,
                (By.CSS_SELECTOR, _loc_funcionario.format(i))
            ))
        return funcs

class FuncionarioFatura(Funcionario):
    """Funcionario contém todas as informações dos terceirizados."""
    dias_trabalhados = None
    salario_base = None
    salario_total = None
    demais_informacoes = None
    
    def __init__(self, webdriver, _loc_funcionario, dados=None):
        super().__init__(webdriver, _loc_funcionario)
        # Seletores
        self._loc_dias_trabalhados = (
            By.CSS_SELECTOR,
            _loc_funcionario[1] + ' ' + 'td:nth-child(6) input'
        )
        self._loc_salario_base = (
            By.CSS_SELECTOR,
            _loc_funcionario[1] + ' ' + 'td:nth-child(7) input'
        )
        self._loc_salario_total = (
            By.CSS_SELECTOR,
            _loc_funcionario[1] + ' ' + 'td:nth-child(13) input'
        )
        self._loc_demais_informacoes = (
            By.CSS_SELECTOR,
            _loc_funcionario[1] + ' ' + 'button'
        )
        self._load_data()

    def preencher_dias_trabalhados(self, valor):
        self._digitar_pagina_principal(self._loc_dias_trabalhados, valor)

    def preencher_salario_base(self, valor):
        self._digitar_pagina_principal(self._loc_salario_base, valor)

    def ir_para_demais_informacoes(self):
        self._clicar(self._loc_demais_informacoes)
        try:
            self.demais_informacoes = DemaisInformacoes(self.webdriver)
        except exception:
            print('Problema com substituto')

    def _digitar_pagina_principal(self, locator, valor):
        self._digitar(locator, valor)
        self._clicar(self._loc_cpf)
        self._esperar_carregamento()
        self._load_data()

    def _load_data(self):
        self.dias_trabalhados = self._load_atrib_value(self._loc_dias_trabalhados)
        self.salario_base = self._load_atrib_value(self._loc_salario_base)
        self.salario_total = self._load_atrib_value(self._loc_salario_total)

    def __repr__(self):
        return f'Funcionario(nome="{self.nome}", cpf="{self.cpf}")'


class DemaisInformacoes(TypeAgent):
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self._loc_aba_montanteA = (By.CSS_SELECTOR, 'li.nav-item:nth-child(1) a')
        self._loc_aba_montanteB = (By.CSS_SELECTOR, 'li.nav-item:nth-child(2) a')
        self._loc_aba_montanteC = (By.CSS_SELECTOR, 'li.nav-item:nth-child(3) a')
        self._loc_aba_provisionamento = (By.CSS_SELECTOR, 'li.nav-item:nth-child(4) a')

        self._loc_tabela_montanteA = (By.CSS_SELECTOR, 'tab.tab-pane:nth-child(1) tbody')
        self._loc_tabela_montanteB = (By.CSS_SELECTOR, 'tab.tab-pane:nth-child(2) tbody')
        self._loc_tabela_montanteC = (By.CSS_SELECTOR, 'tab.tab-pane:nth-child(3) tbody')
        self._loc_tabela_provisionamento_hora_extra = (
            By.CSS_SELECTOR,
            'tab.tab-pane:nth-child(4) > table:nth-child(1) > tbody'
        )
        self._loc_tabela_provisionamento_viagem = (
            By.CSS_SELECTOR,
            'tab.tab-pane:nth-child(4) > table:nth-child(2) > tbody'
        )
        self._loc_fechar = (By.CSS_SELECTOR, '.modal-footer button')

    def preencher_montante_A(self, dados):
        self._preencher(self._loc_tabela_montanteA, dados)
    
    def preencher_montante_B(self, dados):
        self._preencher(self._loc_tabela_montanteB, dados)

    def preencher_montante_C(self, dados):
        self._preencher(self._loc_tabela_montanteC, dados)
    
    def preencher_provisionamento_hora_extra(self, dados):
        self._preencher(self._loc_tabela_provisionamento_hora_extra, dados)

    def preencher_provisionamento_viagem(self, dados):
        self._preencher(self._loc_tabela_provisionamento_viagem, dados)
    
    def ir_para_montanteA(self):
        self._ir_para(self._loc_aba_montanteA)

    def ir_para_montanteB(self):
        self._ir_para(self._loc_aba_montanteB)

    def ir_para_montanteC(self):
        self._ir_para(self._loc_aba_montanteC)
        
    def ir_para_provisionamento(self):
        self._ir_para(self._loc_aba_provisionamento)
    
    def fechar_janela(self):
        self._clicar(self._loc_fechar)
        self._esperar_carregamento()

    def _ir_para(self, aba):
        self._clicar(aba)

    def _preencher(self, loc_tabela, dados):
        _loc_inputs = self._listar_loc_inputs(loc_tabela)
        tabela = self.find_element(loc_tabela)

        for row, _loc_input in zip(tabela.find_elements(By.TAG_NAME, 'tr'), _loc_inputs):
            descricao = row.find_element(By.TAG_NAME, 'td').text
            try:
                self._digitar(_loc_input, dados[descricao])
            except KeyError:
                ...

    def _listar_loc_inputs(self, loc_tabela):
        complemento = ' ' + 'input'
        num_inputs = len(self.find_elements(
            (loc_tabela[0], loc_tabela[1] + complemento)
        ))
        complemento = ' ' + '> tr:nth-child({}) input'
        _loc_inputs = []
        for i in range(1, num_inputs + 1):
            _loc_input = (loc_tabela[0], loc_tabela[1] + complemento.format(i))
            if self._input_modificavel(_loc_input):
                _loc_inputs.append(_loc_input)
        return _loc_inputs

    def _input_modificavel(self, locator):
        return not bool(self.find_element(locator).get_attribute('readonly'))