import allure

class TestHeaderNavigation:
    @allure.feature("Навигация")
    @allure.story("Переход по логотипу Яндекса")

    @allure.title("Клик по логотипу Яндекса открывает dzen.ru")
    def test_click_yandex_logo_opens_yandex(self, main_page, base_page):
        with allure.step("Кликнуть по логотипу Яндекса"):
            main_page.click_element(main_page.LOGO_YANDEX)
        with allure.step("Дождаться появления второй вкладки и переключиться на неё"):
            main_page.wait.until(lambda d: len(d.window_handles) > 1)
            base_page.switch_to_window()
        with allure.step("Проверить, что URL содержит dzen.ru"):
            main_page.wait.until(lambda d: "dzen.ru" in d.current_url)
            assert "dzen.ru" in base_page.current_url(), "Логотип Яндекса не ведёт на dzen.ru"

    @allure.feature("Навигация")
    @allure.story("Переход по логотипу Самоката")

    @allure.title("Клик по логотипу Самоката возвращает на главную")
    def test_click_scooter_logo_returns_to_main(self, main_page, base_page):
        with allure.step("Кликнуть по верхней кнопке «Заказать», чтобы уйти с главной"):
            main_page.click_element(main_page.ORDER_BUTTON_TOP)
        with allure.step("Кликнуть по логотипу Самоката, чтобы вернуться на главную"):
            main_page.click_element(main_page.LOGO_SCOOTER)
        with allure.step("Дождаться возвращения на главную страницу"):
            main_page.wait.until(lambda d: main_page.BASE_URL in d.current_url)
            assert base_page.current_url().endswith("/"), "Логотип Самоката не возвращает на главную"
