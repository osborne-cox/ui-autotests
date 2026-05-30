import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

VALID_USER = "standard_user"
VALID_PASSWORD = "secret_sauce"


class TestCart:
    """Тесты корзины: добавление товаров и выход."""

    @pytest.fixture(autouse=True)
    def login(self, page):
        # Предусловие для всех тестов класса: пользователь авторизован.
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(VALID_USER, VALID_PASSWORD)

    def test_add_one_item(self, page):
        """Один товар → счётчик корзины = 1."""
        inventory = InventoryPage(page)

        assert inventory.get_cart_count() == 0, \
            "Корзина должна быть пустой перед тестом"

        inventory.add_backpack_to_cart()

        assert inventory.get_cart_count() == 1, \
            f"Ожидали 1 товар, получили {inventory.get_cart_count()}"

    def test_add_two_items(self, page):
        """Два товара → счётчик = 2."""
        inventory = InventoryPage(page)

        inventory.add_backpack_to_cart()
        inventory.add_bike_light_to_cart()

        assert inventory.get_cart_count() == 2, \
            f"Ожидали 2 товара, получили {inventory.get_cart_count()}"

    def test_logout(self, page):
        """Выход → возврат на страницу логина."""
        inventory = InventoryPage(page)
        inventory.logout()

        expected_url = LoginPage.URL
        assert page.url.rstrip('/') == expected_url.rstrip('/'), \
            f"После логаута ожидали {expected_url}, получили {page.url}"
