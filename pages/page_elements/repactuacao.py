from page_objects import PageElement
from pages.page_elements.funcionario import Funcionario
from selenium.webdriver.common.by import By

class TerceirizadosRepactuacao(PageElement):
    _loc_tabela_terceirizados = (By.CSS_SELECTOR, '#gridPrincipal > table > tbody')
# div.table-responsive:nth-child(4) > table:nth-child(1) > tbody:nth-child(2)
    funcionarios = []

    def carregar_funcionarios(self, dados):
        self.funcionarios = self._listar_funcionarios_cadastrados()
        self._atribuir_dados_funcionarios(dados)

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

    def _atribuir_dados_funcionarios(self, dados):
        for func in self.funcionarios:
            if func.cpf in dados.keys():
                    func.dados = dados[func.cpf]

class FuncionarioRepactuacao(Funcionario):
    '''''' 
    provisionamento = None

    def __init__(self, webdriver, _loc_funcionario):
        super().__init__(webdriver, _loc_funcionario)
        # Seletores
        self._loc_provisionamento = (
            By.CSS_SELECTOR,
            _loc_funcionario[1] + ' td:nth-child(7) input'
        )
        self._load_data()
    
    def preencher_provisionamento(self, valor):
        self._digitar_pagina_principal(self._loc_provisionamento, valor)
    
    def _digitar_pagina_principal(self, locator, valor):
        self._digitar(locator, valor)
        self._clicar(self._loc_cpf)
        self._esperar_carregamento()
        self._load_data()
    
    def _load_data(self):
        self.provisionamento = self._load_atrib_value(self._loc_provisionamento)
