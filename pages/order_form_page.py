from datetime import date
import random
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage

class OrderFormPage(BasePage):
    RENTAL_PERIOD_ITEMS = [
        'сутки', 'двое суток', 'трое суток', 'четверо суток',
        'пятеро суток', 'шестеро суток', 'семеро суток'
    ]

    FIELD_NAME = (By.CSS_SELECTOR, "input[placeholder='* Имя']")
    FIELD_SURNAME = (By.CSS_SELECTOR, "input[placeholder='* Фамилия']")
    FIELD_ADDRESS = (By.CSS_SELECTOR, "input[placeholder='* Адрес: куда привезти заказ']")
    FIELD_STATION_INPUT = (By.CSS_SELECTOR, "input[placeholder='* Станция метро']")
    FIELD_PHONE = (By.CSS_SELECTOR, "input[placeholder='* Телефон: на него позвонит курьер']")
    FIELD_COMMENT = (By.CSS_SELECTOR, "input[placeholder='Комментарий для курьера']")
    BTN_NEXT = (By.XPATH, "//button[text()='Далее']")
    MODAL_CONFIRM = (By.CSS_SELECTOR, ".Order_Modal__YZ-d3")
    BTN_CONFIRM_YES = (By.XPATH, "//button[text()='Да']")
    MODAL_SUCCESS_HEADER = (By.CSS_SELECTOR, ".Order_ModalHeader__3FDaJ")
    TEXT_ORDER_NUMBER = (By.XPATH, "//*[contains(@class, 'Order_Text')]")
    FIELD_DELIVERY_DATE = (By.CSS_SELECTOR, "input[placeholder='* Когда привезти самокат']")
    DROPDOWN_RENTAL_TERM = (By.CSS_SELECTOR, ".Dropdown-control")
    DROPDOWN_OPTION = (By.CSS_SELECTOR, ".Dropdown-option")
    COLOR_BLACK = (By.XPATH, "//*[contains(text(), 'чёрный жемчуг')]")
    COLOR_GREY = (By.XPATH, "//*[contains(text(), 'серая безысходность')]")
    BTN_ORDER_SUBMIT = (By.XPATH, "//div[contains(@class, 'Order_Buttons')]//button[text()='Заказать']")

    @allure.step("Дождаться загрузки формы заказа (поле «Имя» готово к вводу)")
    def wait_for_form_to_load(self):
        el = self.wait.until(EC.element_to_be_clickable(self.FIELD_NAME))
        return el

    @allure.step("Заполнить поле «Имя»: {name}")
    def fill_name(self, name: str):
        el = self.wait_until_ready_for_input(self.FIELD_NAME)
        el.clear()
        el.send_keys(name)

    @allure.step("Заполнить поле «Фамилия»: {surname}")
    def fill_surname(self, surname: str):
        el = self.wait_until_ready_for_input(self.FIELD_SURNAME)
        el.clear()
        el.send_keys(surname)

    @allure.step("Заполнить поле «Адрес»: {address}")
    def fill_address(self, address: str):
        el = self.wait_until_ready_for_input(self.FIELD_ADDRESS)
        el.clear()
        el.send_keys(address)

    @allure.step("Выбрать станцию метро: {station}")
    def select_station_by_text(self, station: str):
        input_el = self.wait_until_ready_for_input(self.FIELD_STATION_INPUT)
        ActionChains(self.driver).move_to_element(input_el).click().perform()
        input_el.clear()
        input_el.send_keys(station)
        suggestion_locator = (
            By.CSS_SELECTOR,
            ".select-search__list div, "
            ".select-search__option, "
            "li[role='option'], "
            "div[role='option']"
        )
        options = self.wait.until(
            EC.presence_of_all_elements_located(suggestion_locator),
            message=f"Не появились опции для станции '{station}'"
        )
        target_option = None
        station_lower = station.lower()
        for opt in options:
            if station_lower in opt.text.lower():
                target_option = opt
                break
        if target_option:
            self.wait.until(EC.element_to_be_clickable(target_option))
            target_option.click()
        else:
            input_el.send_keys(u'\ue007')  # Enter

    @allure.step("Заполнить поле «Телефон»: {phone}")
    def fill_phone(self, phone: str):
        el = self.wait_until_ready_for_input(self.FIELD_PHONE)
        el.clear()
        el.send_keys(phone)

    @allure.step("Заполнить комментарий для курьера: {comment}")
    def fill_comment(self, comment: str):
        if not comment:
            return
        el = self.wait_until_ready_for_input(self.FIELD_COMMENT)
        el.clear()
        el.send_keys(comment)

    @allure.step("Клик по кнопке «Далее»")
    def click_next(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.BTN_NEXT))
        btn.click()

    @allure.step("Установить дату доставки: сегодня (dd.MM.YYYY)")
    def set_delivery_date_today(self):
        today = date.today().strftime("%d.%m.%Y")
        el = self.wait_until_ready_for_input(self.FIELD_DELIVERY_DATE)
        el.clear()
        el.send_keys(today)

    @allure.step("Выбрать срок аренды случайным образом")
    def set_rental_period(self):
        control = self.wait.until(EC.element_to_be_clickable(self.DROPDOWN_RENTAL_TERM))
        control.click()
        options = self.wait.until(EC.presence_of_all_elements_located(self.DROPDOWN_OPTION))
        rental_period = random.choice(self.RENTAL_PERIOD_ITEMS)
        for opt in options:
            if rental_period in opt.text:
                opt.click()
                break

    @allure.step("Выбрать цвет самоката: {color}")
    def select_color_bike(self, color: str):
        color_locator = self.COLOR_BLACK if color == 'black' else self.COLOR_GREY
        color_el = self.wait.until(EC.element_to_be_clickable(color_locator))
        color_el.click()

    @allure.step("Отправить заказ (кнопка «Заказать»)")
    def submit_order(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.BTN_ORDER_SUBMIT))
        btn.click()

    @allure.step("Дождаться появления модального окна подтверждения заказа и кликнуть «Да»")
    def confirm_order_yes(self):
        modal_confirm = self.wait.until(
            EC.visibility_of_element_located(self.MODAL_CONFIRM),
            message="Модальное окно подтверждения заказа не появилось"
        )
        btn_yes = self.wait.until(
            EC.element_to_be_clickable(self.BTN_CONFIRM_YES),
            message="Кнопка «Да» в модальном окне подтверждения не стала кликабельной"
        )
        btn_yes.click()

    @allure.step("Дождаться модального окна «Заказ оформлен» и проверить заголовок")
    def wait_for_success_modal_and_check_header(self):
        header = self.wait.until(
            EC.visibility_of_element_located(self.MODAL_SUCCESS_HEADER),
            message="Модальное окно «Заказ оформлен» не появилось"
        )
        assert "Заказ оформлен" in header.text, f"Не найден текст «Заказ оформлен», заголовок: {header.text}"
        return header

    @allure.step("Дождаться кликабельности элемента")
    def wait_until_ready_for_input(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))
