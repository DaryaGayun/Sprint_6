import pytest
import allure

class TestOrderFlow:
    @pytest.mark.parametrize("name,surname,address,station,phone,comment,color,use_top_button",
        [
            ("Верхняя", "Кнопка", "Адрес, 1", "Сокольники", "+1234567890", "Комментарий 1", "black", True),
            ("Нижняя", "Кнопка", "Адрес, 2", "Чистые пруды", "+0987654321", "Комментарий 2", "grey", False)
        ]
    )
    @allure.feature("Оформление заказа")
    @allure.title("Оформить заказ: {name} {surname}, станция {station}")
    def test_order_success_flow_fixed_values(
        self,
        main_page,
        order_form_page,
        name,
        surname,
        address,
        station,
        phone,
        comment,
        color,
        use_top_button,
    ):
        with allure.step("1. Открыть главную и перейти к форме заказа"):
            main_page.open_main()
            if use_top_button:
                main_page.click_element(main_page.ORDER_BUTTON_TOP)
            else:
                main_page.click_element(main_page.ORDER_BUTTON_FINISH)

        with allure.step("2. Дождаться загрузки формы и заполнить первую часть"):
            order_form_page.wait_for_form_to_load()
            order_form_page.fill_name(name)
            order_form_page.fill_surname(surname)
            order_form_page.fill_address(address)
            order_form_page.select_station_by_text(station)
            order_form_page.fill_phone(phone)

        with allure.step("3. Отправить первую часть формы"):
            order_form_page.click_next()

        with allure.step("4. Заполнить вторую часть формы"):
            order_form_page.select_color_bike(color)
            order_form_page.fill_comment(comment)
            order_form_page.set_rental_period()
            order_form_page.set_delivery_date_today()

        with allure.step("5. Отправить заказ и дождаться модального окна подтверждения"):
            order_form_page.submit_order()
            order_form_page.confirm_order_yes()

        with allure.step("6. Дождаться модального окна и проверить наличия текста «Заказ оформлен»"):
            header = order_form_page.wait_for_success_modal_and_check_header()
            assert "Заказ оформлен" in header.text, "Не найден текст «Заказ оформлен» в модальном окне"
