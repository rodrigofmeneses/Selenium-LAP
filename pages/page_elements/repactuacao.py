from page_objects import PageElement
from pages.page_elements.funcionario import Funcionario
from selenium.webdriver.common.by import By

class TerceirizadosRepactuacao(PageElement):
    # _loc_tabela_terceirizados = (By.CSS_SELECTOR, '#gridPrincipal > table > tbody')
    _loc_tabela_terceirizados = (By.CSS_SELECTOR,'tbody > tr')
    funcionarios = []

    def carregar_funcionarios(self):
        self.funcionarios = self._listar_funcionarios_cadastrados()

    def _listar_funcionarios_cadastrados(self):
        num_funcs = len(self.find_elements(self._loc_tabela_terceirizados))
        funcs = []
        _loc_funcionario = 'tbody > tr:nth-child({})'
        for i in range(1, num_funcs + 1):
            funcs.append(FuncionarioRepactuacao(
                self.webdriver,
                (By.CSS_SELECTOR, _loc_funcionario.format(i))
            ))
        return funcs

class FuncionarioRepactuacao(Funcionario):
    '''''' 
    repactuacao = None

    def __init__(self, webdriver, _loc_funcionario):
        super().__init__(webdriver, _loc_funcionario)
        # Seletores
        self._loc_repactuacao = (
            By.CSS_SELECTOR,
            _loc_funcionario[1] + ' td:nth-child(7) input'
        )
        self._load_data()
    
    def preencher_repactuacao(self, valor):
        self._digitar_pagina_principal(self._loc_repactuacao, valor)
    
    def _digitar_pagina_principal(self, locator, valor):
        self._digitar(locator, valor)
        self._clicar(self._loc_cpf)
        self._esperar_carregamento()
        self._load_data()
    
    def _load_data(self):
        self.repactuacao = self._load_atrib_value(self._loc_repactuacao)
