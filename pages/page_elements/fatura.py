from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from page_objects import PageElement
from time import sleep

class Terceirizados(PageElement):
    _loc_tabela_terceirizados = (By.CSS_SELECTOR, 'tbody > tr')
    funcionarios = []

    def carregar_funcionarios(self, dados):
        self.funcionarios = self._listar_funcionarios_cadastrados()
        self._atribuir_dados_funcionarios(dados)

    def _listar_funcionarios_cadastrados(self):
        num_funcs = len(self.find_elements(self._loc_tabela_terceirizados))
        funcs = []
        _loc_funcionario = 'tbody > tr:nth-child({})'
        for i in range(1, num_funcs + 1):
            funcs.append(Funcionario(
                self.webdriver,
                (By.CSS_SELECTOR, _loc_funcionario.format(i))
            ))
        return funcs

    def _atribuir_dados_funcionarios(self, dados):
        for func in self.funcionarios:
            if func.cpf in dados.keys():
                    func.dados = dados[func.cpf]


class TypeAgent():
    def _digitar(self, locator, valor):
        # uma grande pegadinha é que esse locator é a partir do elemento
        # e não da página.
        elemento = self.find_element(locator)
        # se o valor é o mesmo
        if self._locator_value_equal_data_value(locator, valor):
            # não há nada para digitar
            return
        # Para a digitação deve atentar-se as casas decimais
        if isinstance(valor, int):
        # Caso seja um inteiro, deve adicionar 2 casas decimais
            if valor < 0:
                self._digitar_com_modificador_final(elemento, valor, '00-')
            else:
                self._digitar_com_modificador_final(elemento, valor, '00')
        elif len(str(valor).split('.')[-1]) == 1:
        # Já se o valor tem uma casa decimal, 
        # é necessário um 0 extra, pois 3.20 se torna 0.32
            if valor < 0:
                self._digitar_com_modificador_final(elemento, valor, '0-')
            else:
                self._digitar_com_modificador_final(elemento, valor, '0')
        else:
        # Aqui pode-se digitar normalmente
            if valor < 0:
                self._digitar_com_modificador_final(elemento, valor, '-')
            else:
                self._digitar_com_modificador_final(elemento, valor)
    
    def _locator_value_equal_data_value(self, locator, valor):
        input_value = self._load_atrib_value(locator)
        return input_value == valor

    def _digitar_com_modificador_final(self, elemento, valor, modificador=''):
        elemento.clear()
        elemento.send_keys(
            f"0{str(valor)}{modificador}"
        )
    
    def _load_text(self, locator):
        return self.find_element(locator).text

    def _load_atrib_value(self, locator):
        text = self.find_element(locator).get_attribute('value')
        return float(text.replace('.', '').replace(',', '.'))
    
    def _esperar_carregamento(self):
        wbw = WebDriverWait(self.webdriver, 10)
        try:
            wbw.until_not(
                # lambda webdriver : webdriver.find_element(*(By.CSS_SELECTOR, 'div .block-ui-spinner')).is_displayed()
                expected_conditions.visibility_of_any_elements_located(
                    (By.CSS_SELECTOR, 'div .block-ui-spinner')
            ))
        except ElementClickInterceptedException:
            sleep(3)


class Funcionario(PageElement, TypeAgent):
    def __init__(self, webdriver, _loc_funcionario, dados=None):
        """Funcionario contém todas as informações dos terceirizados."""
        self.webdriver = webdriver
        # Informações
        self.nome = (By.CSS_SELECTOR, _loc_funcionario[1] + ' ' + 'div > span')
        self.cpf = (By.CSS_SELECTOR, _loc_funcionario[1] + ' ' + 'span > span')
        self.dias_trabalhados = (
            By.CSS_SELECTOR,
            _loc_funcionario[1] + ' ' + 'td:nth-child(6) input'
        )
        self.salario_base = (
            By.CSS_SELECTOR,
            _loc_funcionario[1] + ' ' + 'td:nth-child(7) input'
        )
        self.salario_total = (
            By.CSS_SELECTOR,
            _loc_funcionario[1] + ' ' + 'td:nth-child(13) input'
        )
        self.demais_informacoes = (
            By.CSS_SELECTOR,
            _loc_funcionario[1] + ' ' + 'button'
        )
        self.dados = dados
        # Seletores
        self._loc_funcionario = _loc_funcionario
        self._loc_nome = self.nome
        self._loc_cpf = self.cpf
        self._loc_dias_trabalhados = self.dias_trabalhados
        self._loc_salario_base = self.salario_base
        self._loc_salario_total = self.salario_total
        self._loc_demais_informacoes = self.demais_informacoes
        self._load()
    
    def is_total_compativel(self):
        self._load()
        return self.dados.salario_total == self.salario_total

    def preencher_dias_trabalhados(self, valor):
        self._digitar_pagina_principal(self._loc_dias_trabalhados, valor)

    def preencher_salario_base(self, valor):
        self._digitar_pagina_principal(self._loc_salario_base, valor)

    def ir_para_demais_informacoes(self):
        self._clicar(self._loc_demais_informacoes)
        self.demais_informacoes = DemaisInformacoes(self.webdriver)

    def _digitar_pagina_principal(self, locator, valor):
        self._digitar(locator, valor)
        self._clicar(self._loc_cpf)
        self._esperar_carregamento()
        self._load()

    def _load(self):
        self.nome = self._load_text(self._loc_nome)
        self.cpf = self._load_text(self._loc_cpf)
        self.dias_trabalhados = self._load_atrib_value(self._loc_dias_trabalhados)
        self.salario_base = self._load_atrib_value(self._loc_salario_base)
        self.salario_total = self._load_atrib_value(self._loc_salario_total)

    def __repr__(self):
        return f'Funcionario(nome="{self.nome}", cpf="{self.cpf}")'


class DemaisInformacoes(PageElement, TypeAgent):
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
        self.fechar = (By.CSS_SELECTOR, '.modal-footer button')


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
        self._clicar(self.fechar)
        self._esperar_carregamento()

    def _ir_para(self, aba):
        self._clicar(aba)

    def _preencher(self, loc_tabela, dados):
        _loc_inputs = self._listar_loc_inputs(loc_tabela)
        for _loc_input, value in zip(_loc_inputs, dados):
            self._digitar(_loc_input, value)

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