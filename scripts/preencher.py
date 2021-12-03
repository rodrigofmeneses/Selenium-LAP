from os import path
from time import sleep
from pages.pages import PageFatura
import pandas as pd
import xlwings as xw


class Preencher():
    dados = None
    
    def __init__(self, webdriver, path_dados, intervalo=(10,15), planilha='Plan SPG'):
        self.webdriver = webdriver
        self.pagina = PageFatura(self.webdriver)
        self._carregar_dados(path_dados, intervalo, planilha)

    def run(self):
        funcionarios = self._obter_funcionarios()
        for func in funcionarios:
            if func.is_total_compativel():
                print('Log Positivo')
                continue
            self._preencher_pagina_principal(func)
            self._preencher_demais_funcionarios(func)
    
    
    def _obter_funcionarios(self):
        self.pagina.terceirizados.carregar_funcionarios(self.dados)
        return self.pagina.terceirizados.funcionarios

    def _preencher_pagina_principal(self, func):
        func.preencher_dias_trabalhados(func.dados['Dias Trabalhados'])
        func.preencher_salario_base(func.dados['Salario Base'])

    def _preencher_demais_funcionarios(self, func):
        dados_montanteA = self._segmentar_dados(func.dados, 6, 13)
        dados_montanteB = self._segmentar_dados(func.dados, 13, 25)
        dados_montanteC = self._segmentar_dados(func.dados, 25, 27)
        dados_hora_extra = self._segmentar_dados(func.dados, 27, 33)
        dados_viagem = self._segmentar_dados(func.dados, 33, 38)

        func.ir_para_demais_informacoes()
        fdi = func.demais_informacoes
        fdi.preencher_montante_A(dados_montanteA)
        fdi.ir_para_montanteB()
        fdi.preencher_montante_B(dados_montanteB)
        fdi.ir_para_montanteC()
        fdi.preencher_montante_C(dados_montanteC)
        fdi.ir_para_provisionamento()
        fdi.preencher_provisionamento_hora_extra(dados_hora_extra)
        fdi.preencher_provisionamento_viagem(dados_viagem)
        fdi.fechar_janela()
        sleep(5)

    def _carregar_dados(self, path_dados, intervalo, planilha):
        wb = xw.Book(path_dados)
        sheet = wb.sheets[planilha]

        campos = ['CPF', 'Nome', 'Dias Trabalhados', 'Salario Base', 
            'Salario Total', 'Adicional', 'Adicional Nortuno', 'Reserva', 
            'Encargos', 'Insalibridade', 'Periculosidade', 'Outros', 
            'Vale Transporte', 'Vale Refeicao', 'Taxa', 'Cesta', 'Farda', 
            'Municao', 'Seguro Vida', 'Supervisao', 'IJD', 'IJN', 'Tributos', 
            'Insumos', 'Equipamento', 'Plano Saude', 'Qtd Hora Extra', 
            'Valor Hora Extra', 'DSR', 'Hora Encargos',  'Hora Taxa', 'Hora Tributos', 
            'Qtd Diarias',  'Passagem',  'Viagem', 'Viagem Taxa',  'Viagem Tributos'
        ]

        self.dados = pd.DataFrame(columns=campos)

        for i in range(*intervalo):
            valores_func = []
            valores_func += [sheet[f'U{i}'].value] # CPF
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
            valores_func += [sheet[f'L{i}'].value] # Vale Alimentacao
            valores_func += [sheet[f'J{i}'].value] # Taxa
            valores_func += [sheet[f'N{i}'].value] # Cesta
            valores_func += [sheet[f'M{i}'].value] # Farda
            valores_func += [0.] * 5
            valores_func += [sheet[f'O{i}'].value] # Tributos
            valores_func += [0.] * 2
            valores_func += [sheet[f'P{i}'].value] # Plano de saude
            valores_func += [0.] * 11
            s = pd.Series(valores_func, index=campos)
            self.dados = self.dados.append(s, ignore_index=True)
        # valores_func
        self.dados = self.dados.fillna(0.)

        for i in range(self.dados.shape[0]):
            if self.dados.iloc[i]['Salario Total'] == 0.:
                for c in self.dados.columns[2:]:
                    self.dados.at[i, c] = 0.

        self.dados = self.dados.set_index('CPF')
    
    def _segmentar_dados(self, dados, i, j):
        return dados[i:j]
