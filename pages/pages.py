from page_objects import Page
from pages.page_elements.login import Login
from pages.page_elements.guardiao import Planejamento
from pages.page_elements.spg import MenuSuperior, MenuLateral, Avisos
from pages.page_elements.fatura import TerceirizadosFatura
from pages.page_elements.repactuacao import TerceirizadosRepactuacao


class PageLogin(Page):
    login = Login()


class PageGuardiao(Page):
    planejamento = Planejamento()


class PageSPG(Page):
    menu_superior = MenuSuperior()
    menu_lateral = MenuLateral()
    avisos = Avisos()


class PageFatura(Page):
    terceirizados = TerceirizadosFatura()


class PageRepactuacao(Page):
    terceirizados = TerceirizadosRepactuacao()
