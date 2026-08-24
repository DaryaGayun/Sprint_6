from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

class BasePage:
    @allure.step("Инициализация драйвера")
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Кликнуть по пункту аккордеона: индекс={locator}")
    def find_element(self, locator):
        """Ждёт и возвращает видимый элемент по локатору."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Кликнуть по пункту аккордеона: индекс={locator}")
    def click_element(self, locator):
        el = self.find_element(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
            el
        )
        clickable_el = self.wait.until(EC.element_to_be_clickable(el))
        clickable_el.click()

    @allure.step("Кликнуть по пункту аккордеона: индекс={locator}")
    def get_text(self, locator):
        """Возвращает текст элемента."""
        return self.find_element(locator).text.strip()

    @allure.step("Кликнуть по пункту аккордеона: индекс={locator}")
    def is_visible(self, locator):
        """Проверяет видимость элемента (возвращает True/False)."""
        try:
            self.wait.until(EC.visibility_of_element_located(locator), timeout=3)
            return True
        except Exception:
            return False

    @allure.step("Открыть страниу: url={url}")
    def open(self, url):
        self.driver.get(url)

    @allure.step("прокручивает страницу так, чтобы указанный элемент оказался по центру экрана: элемент={elem}")
    def scroll_into_view(self, elem):
        self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                    elem
                )

    @allure.step("Переключиться на последнюю открытую вкладку")
    def switch_to_window(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])

    @allure.step("Получить URL текущей страницы")
    def current_url(self):
        return self.driver.current_url

    @allure.step("Проверяет, что текущий URL заканчивается на указанный суффикс: суффикс={suffix}")
    def url_ends_with(self, suffix: str) -> bool:
        """Проверяет, что текущий URL заканчивается на указанный суффикс."""
        return self.driver.current_url.endswith(suffix)
