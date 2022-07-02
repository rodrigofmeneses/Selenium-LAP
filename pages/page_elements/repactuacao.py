from page_objects import PageElement
from selenium.webdriver.common.by import By

class TerceirizadosRepactuacao(PageElement):
    _loc_tabela_terceirizados = (By.CSS_SELECTOR, '#gridPrincipal > table > tbody')
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






