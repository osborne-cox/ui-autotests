from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

# saucedemo заранее заводит разные типы юзеров под тесты.
VALID_USER = "standard_user"
LOCKED_USER = "locked_out_user"
VALID_PASSWORD = "secret_sauce"
WRONG_PASSWORD = "wrong123"


class TestLogin:

    def test_successful_login(self, page):
        """Позитивный: корректные данные → попадаем на страницу товаров."""
        login_page = LoginPage(page)
        login_page.open()

        login_page.login(VALID_USER, VALID_PASSWORD)

        inventory = InventoryPage(page)
        assert inventory.is_loaded(), (
            f"После логина ожидали {InventoryPage.URL}, получили {page.url}"
        )

    def test_login_wrong_password(self, page):
        """Негативный: неверный пароль → отображается ошибка с нужным текстом."""
        login_page = LoginPage(page)
        login_page.open()

        login_page.login(VALID_USER, WRONG_PASSWORD)

        assert login_page.is_error_visible(), \
            "Ошибка не появилась после неверного пароля"

        error_text = login_page.get_error_text()
        assert "Username and password do not match" in error_text, \
            f"Неожиданный текст ошибки: '{error_text}'"

    def test_login_locked_user(self, page):
        """Негативный: заблокированный аккаунт → ошибка о блокировке."""
        login_page = LoginPage(page)
        login_page.open()

        login_page.login(LOCKED_USER, VALID_PASSWORD)

        error_text = login_page.get_error_text()
        assert "locked out" in error_text.lower(), \
            f"Ожидали сообщение о блокировке, получили: '{error_text}'"
