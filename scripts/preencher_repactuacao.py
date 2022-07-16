from pages.pages import PageRepactuacao
from openpyxl import load_workbook

class PreencherRepactuacao():
    '''Classe responsável por preencher os campos dos funcionários na Página de Repactuação.
    
    Args:
        webdriver: Objeto Selenium
        caminho_dados: Caminho do arquivo de dados.
        intervalo_funcionarios: Intervalo das células onde estão os funcionarios.
        nome_planilha: Nome da planilha.
        
    '''    
    def __init__(self, webdriver, caminho_dados, intervalo_funcionarios, nome_planilha):
        self.webdriver = webdriver
        self.pagina = PageRepactuacao(self.webdriver)
        self.dados = self._carregar_dados(caminho_dados, intervalo_funcionarios, nome_planilha)
    
    def run(self, inicio=0):
        funcionarios = self._obter_funcionarios()
        func_atual = inicio
        for func in funcionarios[inicio:]:
            print(func_atual, func.nome, func.cpf)
            func_atual += 1
            if not func.cpf in self.dados.keys():
                print('Funcionário não está na planilha')
                continue
            if self._repactuacao_compativel(func):
                print('Total compatível!')
                continue
            self._preencher_pagina_principal(func)
            
            func._load_data()
            if self._repactuacao_compativel(func):
                print('Total compatível!')
            else:
                print('Total incompatível. Algo está errado')
                print('-' * 20)
    
    
    def _obter_funcionarios(self):
        '''Obtem a lista de funcionários a partir da tabela de terceirazados
        na página de fatura e a retorna.
        '''
        self.pagina.terceirizados.carregar_funcionarios()
        return self.pagina.terceirizados.funcionarios

    def _preencher_pagina_principal(self, func):
        '''Preenche os campos da página principal, os dias trabalhados
        e o salário base. Ambos tem uma maneira semelhante de preenchimento.
        '''
        func.preencher_repactuacao(self.dados[func.cpf]['repactuacao'])

    def _carregar_dados(self, caminho_dados, intervalo_funcionarios, nome_planilha):
        '''Carregar os dados do arquivo excel especificado.
        
        Atenção, apenas formato xlsx

        O arquivo será aberto e direcionado a planilha especificada.
        Os campos das colunas será associado a um pandas data frame.
        Será percorrido todo o intervalo de funcionários e preenchido
        uma linha por vez dos dados.
        Os funcionários com Salário zerado terão todos os campos zerados,
        isso significa que o funcionário ou foi demitido, ou está de férias.
        Por fim, associa-se os indices aos CPFs e retorna os dados.
        '''
        wb = load_workbook(caminho_dados, data_only=True)
        sheet = wb[nome_planilha]

        dados = {}
        for i in range(*intervalo_funcionarios):
            cpf = sheet[f'U{i}'].value # CPF
            if not cpf:
                print('Funcionário sem cpf')
                continue 
            valores = {
                'nome': sheet[f'A{i}'].value,
                'cpf': cpf,
                'repactuacao': sheet[f'S{i}'].value,
            }

            # Trocar valores nulos por 0.
            for chave, valor in valores.items():
                if not valor:
                    valores[chave] = 0.
            
            dados[cpf] = valores
        return dados
    
    def _repactuacao_compativel(self, funcionario):
        '''Verifica se o salário total do funcionário está compatível
            funcionario: Funcionário a ser verificado
        '''
        return funcionario.repactuacao == self.dados[funcionario.cpf]['repactuacao']
    