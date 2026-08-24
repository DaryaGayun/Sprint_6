import pytest
import allure
from selenium import webdriver
from pages.base_page import BasePage
from pages.main_page import MainPage
from pages.order_form_page import OrderFormPage

@pytest.fixture(scope="function")
def driver():
    options = webdriver.FirefoxOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Firefox(options=options)
    yield driver
    driver.quit()
    
@pytest.fixture
def base_page(driver):
    return BasePage(driver)

@pytest.fixture
def main_page(driver):
    page = MainPage(driver)
    with allure.step("Открыть главную страницу"):
        page.open_main()
    return page

@pytest.fixture
def order_form_page(driver):
    return OrderFormPage(driver)
