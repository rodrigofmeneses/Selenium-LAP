from page_objects import Page
from .elements import (
    Login, Planejamento, MenuSuperior, MenuLateral, 
    Avisos, Terceirizados)


class PageLogin(Page):
    login = Login()


class PageGuardiao(Page):
    planejamento = Planejamento()


class PageSPG(Page):
    menu_superior = MenuSuperior()
    menu_lateral = MenuLateral()
    avisos = Avisos()


class PageFatura(Page):
    terceirizados = Terceirizados()
