from pages.pages import PageLogin, PageGuardiao, PageSPG, PageFatura


class Inicializar():
    pagina = None

    def __init__(self, webdriver, url, credenciais):
        self.webdriver = webdriver
        self.url = url
        self.credenciais = credenciais

    def run(self):
        self._login()
        self._guardiao()
        self._spg()
        return PageFatura(self.webdriver)
        
    def _login(self):
        self.pagina = PageLogin(self.webdriver, self.url)
        self.pagina.open()
        self.pagina.login.logar(self.credenciais)
    
    def _guardiao(self):
        self.pagina = PageGuardiao(self.webdriver)
        self.pagina.planejamento.acessar_spg()
    
    def _spg(self):
        self.pagina = PageSPG(self.webdriver)
        self.pagina.menu_superior.clicar_sister()
        self.pagina.avisos.fechar_avisos()
        self.pagina.menu_lateral.clicar_fatura()
        self.pagina.menu_lateral.clicar_controle_de_fatura()