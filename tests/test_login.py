from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

# Тестовые данные — в одном месте
# saucedemo.com специально сделал разные типы юзеров для тест-кейсов
VALID_USER     = "standard_user"    # Обычный юзер, всё работает
LOCKED_USER    = "locked_out_user"  # Заблокирован — для теста ошибки блокировки
VALID_PASSWORD = "secret_sauce"
WRONG_PASSWORD = "wrong123"


class TestLogin:
    """
    Класс группирует связанные тесты.
    Называем по фиче: TestLogin, TestCart, TestCheckout.
    """

    def test_successful_login(self, page):
        """
        ✅ ПОЗИТИВНЫЙ: корректные данные → попадаем на страницу товаров

        AAA-паттерн (стандарт написания тестов):
        Arrange — подготовка окружения
        Act     — выполнение действия
        Assert  — проверка результата
        """
        # Arrange
        login_page = LoginPage(page)
        login_page.open()

        # Act
        login_page.login(VALID_USER, VALID_PASSWORD)

        # Assert
        inventory = InventoryPage(page)
        assert inventory.is_loaded(), (
            f"После логина ожидали URL {InventoryPage.URL}, "
            f"получили {page.url}"
        )
        # assert condition, message
        # Если condition = False → тест падает с сообщением

    def test_login_wrong_password(self, page):
        """
        ❌ НЕГАТИВНЫЙ: неверный пароль → ошибка отображается
        Проверяем что система корректно обрабатывает некорректный ввод
        """
        login_page = LoginPage(page)
        login_page.open()

        login_page.login(VALID_USER, WRONG_PASSWORD)

        # Шаг 1: ошибка вообще появилась?
        assert login_page.is_error_visible(), \
            "Ошибка не появилась после неверного пароля"

        # Шаг 2: текст ошибки правильный?
        error_text = login_page.get_error_text()
        assert "Username and password do not match" in error_text, \
            f"Неожиданный текст ошибки: '{error_text}'"

    def test_login_locked_user(self, page):
        """
        🔒 НЕГАТИВНЫЙ: заблокированный аккаунт → специфическая ошибка
        Проверяем что блокировка работает и сообщает правильную причину
        """
        login_page = LoginPage(page)
        login_page.open()

        login_page.login(LOCKED_USER, VALID_PASSWORD)

        error_text = login_page.get_error_text()
        assert "locked out" in error_text.lower(), (
            f"Ожидали сообщение о блокировке, получили: '{error_text}'"
        )
        # .lower() — приводим к нижнему регистру чтобы не зависеть от Locked/locked
