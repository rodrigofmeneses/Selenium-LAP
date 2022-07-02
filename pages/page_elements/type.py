from page_objects import PageElement
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from time import sleep

class TypeAgent(PageElement):
    '''
    Classe para auxíliar objetos que precisem digitar.
    '''
    def _digitar(self, locator, valor):
        # uma grande pegadinha é que esse locator é a partir do elemento
        # e não da página.
        elemento = self.find_element(locator)
        # se o valor é o mesmo
        if self._locator_value_equal_data_value(locator, valor):
            # não há nada para digitar
            return
        # Para a digitação deve atentar-se as casas decimais
        if isinstance(valor, int):
        # Caso seja um inteiro, deve adicionar 2 casas decimais
            if valor < 0:
                self._digitar_com_modificador_final(elemento, valor, '00-')
            else:
                self._digitar_com_modificador_final(elemento, valor, '00')
        elif len(str(valor).split('.')[-1]) == 1:
        # Já se o valor tem uma casa decimal, 
        # é necessário um 0 extra, pois 3.20 se torna 0.32
            if valor < 0:
                self._digitar_com_modificador_final(elemento, valor, '0-')
            else:
                self._digitar_com_modificador_final(elemento, valor, '0')
        else:
        # Aqui pode-se digitar normalmente
            if valor < 0:
                self._digitar_com_modificador_final(elemento, valor, '-')
            else:
                self._digitar_com_modificador_final(elemento, valor)
    
    def _locator_value_equal_data_value(self, locator, valor):
        input_value = self._load_atrib_value(locator)
        return input_value == valor

    def _digitar_com_modificador_final(self, elemento, valor, modificador=''):
        elemento.clear()
        elemento.send_keys(
            f"0{str(valor)}{modificador}"
        )
    
    def _load_text(self, locator):
        return self.find_element(locator).text

    def _load_atrib_value(self, locator):
        text = self.find_element(locator).get_attribute('value')
        return float(text.replace('.', '').replace(',', '.'))
    
    def _esperar_carregamento(self):
        wbw = WebDriverWait(self.webdriver, 10)
        try:
            wbw.until_not(
                # lambda webdriver : webdriver.find_element(*(By.CSS_SELECTOR, 'div .block-ui-spinner')).is_displayed()
                expected_conditions.visibility_of_any_elements_located(
                    (By.CSS_SELECTOR, 'div .block-ui-spinner')
            ))
        except ElementClickInterceptedException:
            sleep(3)
