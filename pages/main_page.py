from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage
import allure

class MainPage(BasePage):
    BASE_URL = "https://qa-scooter.praktikum-services.ru/"

    LOGO_YANDEX = (By.CSS_SELECTOR, "a.Header_LogoYandex__3TSOI")
    LOGO_SCOOTER = (By.CSS_SELECTOR, "a.Header_LogoScooter__3lsAR")
    ORDER_BUTTON_TOP = (By.XPATH, "//div[contains(@class, 'Header_Nav')]//button[normalize-space()='Заказать']")
    ORDER_BUTTON_FINISH = (By.XPATH, "//div[contains(@class, 'Home_FinishButton')]//button[normalize-space()='Заказать']")
    COOKIE_BANNER = (By.CSS_SELECTOR, ".App_CookieConsent__1yUIN")
    COOKIE_ACCEPT = (By.ID, "rcc-confirm-button")
    ACCORDION_BUTTONS = (By.CSS_SELECTOR, ".accordion__button")
    ACCORDION_HEADING_ID_TEMPLATE = "accordion__heading-{}"
    ACCORDION_PANEL_ID_TEMPLATE = "accordion__panel-{}"

    @allure.step("Открыть главную страницу и дождаться логотипа самоката")
    def open_main(self):
        self.open(self.BASE_URL)
        self.wait.until(EC.visibility_of_element_located(self.LOGO_SCOOTER))

    @allure.step("Получить кнопку аккордеона по индексу: индекс={index}")
    def get_accordion_button_by_index(self, index):
        buttons = self.wait.until(EC.presence_of_all_elements_located(self.ACCORDION_BUTTONS))
        if index < 0 or index >= len(buttons):
            raise IndexError(f"Аккордеон имеет только {len(buttons)} пунктов, индекс {index} вне диапазона")
        return buttons[index]

    @allure.step("Скроллить к секции FAQ")
    def scroll_to_faq_section(self):
        faq_section_locator = (By.CSS_SELECTOR, ".Home_FAQ__3uVm4")
        el = self.find_element(faq_section_locator)
        self.scroll_into_view(el)

    @allure.step("Кликнуть по пункту аккордеона: индекс={index}")
    def click_accordion_item(self, index):
        btn = self.get_accordion_button_by_index(index)
        actions = ActionChains(self.driver)
        actions.move_to_element(btn).perform()
        heading_locator = (By.ID, self.ACCORDION_HEADING_ID_TEMPLATE.format(index))
        self.wait.until(EC.element_to_be_clickable(heading_locator))
        btn.click()

    @allure.step("Проверить, что панель аккордеона открыта по атрибуту hidden: индекс={index}")
    def is_accordion_panel_opened_by_hidden(self, index):
        panel_locator = (By.ID, self.ACCORDION_PANEL_ID_TEMPLATE.format(index))
        panel = self.find_element(panel_locator)
        hidden_attr = panel.get_attribute("hidden")
        return hidden_attr is None or hidden_attr == ""

    @allure.step("Получить текст ответа из панели аккордеона: индекс={index}")
    def get_answer_text_by_index(self, index):
        panel_locator = (By.ID, self.ACCORDION_PANEL_ID_TEMPLATE.format(index))
        panel = self.find_element(panel_locator)
        text_el = panel.find_element(By.TAG_NAME, "p")
        return text_el.text.strip()

    @allure.step("Полностью проверить аккордеон по индексу: открыть и сравнить текст. Ожидаемый текст: {expected_answer}")
    def verify_accordion_full(self, index: int, expected_answer: str) -> bool:
        self.click_accordion_item(index)
        if not self.is_accordion_panel_opened_by_hidden(index):
            return False
        actual_answer = self.get_answer_text_by_index(index)
        return actual_answer == expected_answer
