from page_objects import Page
from .elements import Login, Planejamento, Terceirizados


class PageLogin(Page):
    login = Login()


class PageGuardiao(Page):
    planejamento = Planejamento()


class PageFatura(Page):
    terceirizados = Terceirizados()
