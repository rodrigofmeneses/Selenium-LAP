from pages.pages import PageFatura
from collections import namedtuple, OrderedDict
from openpyxl import load_workbook

class Preencher():
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
                # continue
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

        Inicialmente os dados serão segmentados para que seja 
        preenchida aba por aba.

        Em seguida o botão das demais informações deve ser
        clicado e ao alcançar a próxima janela deve seguir a
        ordem - preencher - ir para outra aba - preencher.

        Ao fim, fechar a janela.
        """

        def segmentar_dados(dados, i, j):
            return dados[i:j]

        dados_montanteA = segmentar_dados(func.dados, 5, 12)
        dados_montanteB = segmentar_dados(func.dados, 12, 25)
        dados_montanteC = segmentar_dados(func.dados, 25, 26)
        # dados_hora_extra = segmentar_dados(func.dados, 27, 32)
        # dados_viagem = segmentar_dados(func.dados, 32, 37)

        func.ir_para_demais_informacoes()
        fdi = func.demais_informacoes
        fdi.preencher_montante_A(dados_montanteA)
        fdi.ir_para_montanteB()
        fdi.preencher_montante_B(dados_montanteB)
        fdi.ir_para_montanteC()
        fdi.preencher_montante_C(dados_montanteC)
        # fdi.ir_para_provisionamento()
        # fdi.preencher_provisionamento_hora_extra(dados_hora_extra)
        # fdi.preencher_provisionamento_viagem(dados_viagem)
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

        # configuração para sps
        campos = '''
            cpf
            nome
            dias_trabalhados
            salario_base
            salario_total
            adicional
            adicional_noturno
            reserva
            encargos
            insalubridade
            periculosidade
            outros 
            vale_transporte
            vale_refeicao
            taxa
            cesta
            farda 
            municao
            seguro_vida
            supervisao
            plano_saude
            ijd
            ijn
            tributos
            insumos 
            equipamento
            qtd_hora_extra
            valor_hora_extra
            dsr
            hora_encargos
            hora_taxa
            hora_tributos 
            qtd_diarias
            passagem
            viagem
            viagem_taxa
            viagem_tributos
        '''

        dados = OrderedDict()
        Func = namedtuple('Funcionario', campos)

        for i in range(*intervalo_funcionarios):
            valores_func = []
            cpf = sheet[f'U{i}'].value # CPF
            if not cpf:
                continue 
            valores_func += [cpf] # CPF
            valores_func += [sheet[f'A{i}'].value] # Nome
            valores_func += [sheet[f'C{i}'].value] # Dias
            valores_func += [sheet[f'E{i}'].value] # Salario Base
            valores_func += [sheet[f'R{i}'].value] # Salario Total
            valores_func += [sheet[f'G{i}'].value] # Adicional
            valores_func += [0.] * 2 # Ad noturno - reserva
            valores_func += [sheet[f'H{i}'].value] # Encargos
            valores_func += [0.] # Insalubridade
            valores_func += [sheet[f'F{i}'].value] # Periculosidade
            valores_func += [0.] # Outros
            valores_func += [sheet[f'K{i}'].value] # Vale Transporte
            valores_func += [sheet[f'L{i}'].value] # Vale Refeicao
            valores_func += [sheet[f'J{i}'].value] # Taxa
            valores_func += [sheet[f'N{i}'].value] # Cesta
            valores_func += [sheet[f'M{i}'].value] # Farda
            valores_func += [0.] * 3
            valores_func += [sheet[f'O{i}'].value] # Plano de saude
            valores_func += [0.] * 2
            valores_func += [sheet[f'P{i}'].value] # Tributos
            valores_func += [0.] * 13

            valores_func = [valor if bool(valor) and valores_func[4] != 0. else 0.
                            for valor in valores_func]
            
            func = Func(*valores_func)
            dados[func.cpf] = func

        return dados
    
    
