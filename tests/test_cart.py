import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

VALID_USER     = "standard_user"
VALID_PASSWORD = "secret_sauce"


class TestCart:
    """Тесты корзины — добавление товаров и выход"""

    @pytest.fixture(autouse=True)
    def login(self, page):
        """
        autouse=True — этот fixture запускается автоматически
        ПЕРЕД каждым тестом в этом классе.

        Зачем: для тестов корзины нужно быть залогиненным.
        Вместо того чтобы писать login() в каждом тесте —
        выносим в fixture.

        Это как preCondition в тест-кейсе:
        "Предусловие: пользователь авторизован"
        """
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(VALID_USER, VALID_PASSWORD)
        # После этого page находится на /inventory.html

    def test_add_one_item(self, page):
        """
        Добавить один товар → счётчик корзины = 1
        """
        inventory = InventoryPage(page)

        # Убеждаемся что корзина пустая в начале теста
        assert inventory.get_cart_count() == 0, \
            "Корзина должна быть пустой перед тестом"

        inventory.add_backpack_to_cart()

        assert inventory.get_cart_count() == 1, \
            f"Ожидали 1 товар, получили {inventory.get_cart_count()}"

    def test_add_two_items(self, page):
        """
        Добавить два товара → счётчик = 2
        Проверяем что счётчик корректно суммирует
        """
        inventory = InventoryPage(page)

        inventory.add_backpack_to_cart()
        inventory.add_bike_light_to_cart()

        assert inventory.get_cart_count() == 2, \
            f"Ожидали 2 товара, получили {inventory.get_cart_count()}"

    def test_logout(self, page):
        """
        Выйти из аккаунта → попадаем обратно на страницу логина
        Проверяем что сессия завершается корректно
        """
        inventory = InventoryPage(page)
        inventory.logout()

        # После логаута должны быть на главной странице (логин)
        expected_url = LoginPage.URL
        assert page.url.rstrip('/') == expected_url.rstrip('/'), \
            f"После логаута ожидали {expected_url}, получили {page.url}"
        # rstrip('/') убирает слэш в конце URL чтобы не было ложного несовпадения
