import re

import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

VALID_USER = "standard_user"
VALID_PASSWORD = "secret_sauce"


class TestCart:
    """Тесты корзины: добавление товаров и выход."""

    @pytest.fixture(autouse=True)
    def login(self, page: Page):
        # Предусловие для всех тестов класса: пользователь авторизован.
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(VALID_USER, VALID_PASSWORD)
        expect(page).to_have_url(InventoryPage.URL)

    def test_add_one_item(self, page: Page):
        """Один товар → счётчик корзины = 1."""
        inventory = InventoryPage(page)

        # На пустой корзине бейджа в DOM нет вообще.
        expect(inventory.cart_badge).to_have_count(0)

        inventory.add_backpack_to_cart()

        expect(inventory.cart_badge).to_have_text("1")

    def test_add_two_items(self, page: Page):
        """Два товара → счётчик = 2."""
        inventory = InventoryPage(page)

        inventory.add_backpack_to_cart()
        inventory.add_bike_light_to_cart()

        expect(inventory.cart_badge).to_have_text("2")

    def test_logout(self, page: Page):
        """Выход → возврат на страницу логина."""
        inventory = InventoryPage(page)
        inventory.logout()

        # saucedemo после логаута редиректит на корень — допускаем слэш в конце.
        expect(page).to_have_url(re.compile(r"saucedemo\.com/?$"))
