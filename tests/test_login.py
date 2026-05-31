from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

# saucedemo заранее заводит разные типы юзеров под тесты.
VALID_USER = "standard_user"
LOCKED_USER = "locked_out_user"
VALID_PASSWORD = "secret_sauce"
WRONG_PASSWORD = "wrong123"


class TestLogin:

    def test_successful_login(self, page: Page):
        """Позитивный: корректные данные → попадаем на страницу товаров."""
        login_page = LoginPage(page)
        login_page.open()

        login_page.login(VALID_USER, VALID_PASSWORD)

        # Веб-first ожидание: ждём нужный URL, а не читаем page.url сразу
        # после клика (иначе ловим состояние до завершения навигации).
        expect(page).to_have_url(InventoryPage.URL)

    def test_login_wrong_password(self, page: Page):
        """Негативный: неверный пароль → ошибка с нужным текстом."""
        login_page = LoginPage(page)
        login_page.open()

        login_page.login(VALID_USER, WRONG_PASSWORD)

        expect(login_page.error_message).to_be_visible()
        expect(login_page.error_message).to_contain_text(
            "Username and password do not match"
        )

    def test_login_locked_user(self, page: Page):
        """Негативный: заблокированный аккаунт → ошибка о блокировке."""
        login_page = LoginPage(page)
        login_page.open()

        login_page.login(LOCKED_USER, VALID_PASSWORD)

        expect(login_page.error_message).to_contain_text("locked out")
