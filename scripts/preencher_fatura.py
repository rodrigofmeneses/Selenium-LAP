from pages.pages import PageFatura
from openpyxl import load_workbook

class PreencherFatura():
    '''Classe responsável por preencher os campos dos funcionários na Página de Fatura.
    
    Args:
        webdriver: Objeto Selenium
        caminho_dados: Caminho do arquivo de dados.
        intervalo_funcionarios: Intervalo das células onde estão os funcionarios.
        nome_planilha: Nome da planilha.
        
    '''    
    def __init__(self, webdriver, caminho_dados, intervalo_funcionarios, nome_planilha):
        self.webdriver = webdriver
        self.pagina = PageFatura(self.webdriver)
        self.dados = self._carregar_dados(caminho_dados, intervalo_funcionarios, nome_planilha)

    def run(self, inicio=0):
        funcionarios = self._obter_funcionarios(self.dados)
        func_atual = inicio
        for func in funcionarios[inicio:]:
            print(func_atual, func.nome, func.cpf)
            func_atual += 1
            if not func.cpf in self.dados.keys():
                print('Funcionário não está na planilha')
                continue
            if func.is_total_compativel():
                print('Total compatível!')
                continue
            self._preencher_pagina_principal(func)
            self._preencher_demais_funcionarios(func)
            
            if func.is_total_compativel():
                print('Total compatível!')
            else:
                print('Total incompatível. Algo está errado')
                print('-' * 20)
    
    
    def _obter_funcionarios(self, dados):
        '''Obtem a lista de funcionários a partir da tabela de terceirazados
        na página de fatura e a retorna.
        '''
        self.pagina.terceirizados.carregar_funcionarios(dados)
        return self.pagina.terceirizados.funcionarios

    def _preencher_pagina_principal(self, func):
        '''Preenche os campos da página principal, os dias trabalhados
        e o salário base. Ambos tem uma maneira semelhante de preenchimento.
        '''
        func.preencher_dias_trabalhados(func.dados.dias_trabalhados)
        func.preencher_salario_base(func.dados.salario_base)

    def _preencher_demais_funcionarios(self, func):
        """Preencher abas demais funcionarios
        func: funcionario que terá abas preenchidas

        O botão das demais informações deve ser
        clicado e ao alcançar a próxima janela deve seguir a
        ordem - preencher - ir para outra aba - preencher.

        Ao fim, fechar a janela.
        """

        func.ir_para_demais_informacoes()
        fdi = func.demais_informacoes
        fdi.preencher_montante_A(self.dados)
        fdi.ir_para_montanteB()
        fdi.preencher_montante_B(self.dados)
        fdi.ir_para_montanteC()
        fdi.preencher_montante_C(self.dados)
        fdi.ir_para_provisionamento()
        fdi.preencher_provisionamento_hora_extra(self.dados)
        fdi.preencher_provisionamento_viagem(self.dados)
        fdi.fechar_janela()

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
                'dias': sheet[f'C{i}'].value,
                'salario_base': sheet[f'E{i}'].value if not None else 0.,
                'salario_total': sheet[f'R{i}'].value if not None else 0.,
                'Valor Adicional': sheet[f'G{i}'].value if not None else 0.,
                'Valor Adicional Noturno': 0.,
                'Valor Reserva Técnica': 0.,
                'Valor Encargos': sheet[f'H{i}'].value if not None else 0.,
                'Valor Insalubridade': 0.,
                'Valor Periculosidade': sheet[f'F{i}'].value if not None else 0.,
                'Valor Outros': 0.,
                'Valor Vale Transporte': sheet[f'K{i}'].value if not None else 0.,
                'Valor Vale Refeição': sheet[f'L{i}'].value if not None else 0.,
                'Valor Taxa': sheet[f'J{i}'].value if not None else 0.,
                'Valor Cesta Basica': sheet[f'N{i}'].value if not None else 0.,
                'Valor Farda': sheet[f'M{i}'].value if not None else 0.,
                'Valor Munição': 0.,
                'Valor Seguro Vida': 0.,
                'Valor Supervisão': 0.,
                'Valor Equipamento': 0.,
                'Valor Plano Saúde': sheet[f'O{i}'].value if not None else 0.,
                'Valor Intra jornada Diurno': 0.,
                'Valor Intra jornada Noturno': 0.,
                'Valor Tributos': sheet[f'P{i}'].value if not None else 0.,
                'Valor Insumos de Mão de Obra': 0.,
                'Quantidade Hora Extra': 0.,
                'Valor Hora Extra': 0.,
                'Valor DSR': 0.,
                'Valor Extra Encargos': 0.,
                'Valor Extra Taxa': 0.,
                'Valor Extra Tributos': 0.,
                'Quantidade Diarias': 0.,
                'Valor Passagem': 0.,
                'Valor Viagem': 0.,
                'Valor Viagem Taxa': 0.,
                'Valor Viagem Tributos': 0.
            }
            if valores['salario_total'] == 0:
                valores = dict.fromkeys(valores, 0)
                valores[cpf] = cpf
            dados[cpf] = valores
        return dados
    
    
