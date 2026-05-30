from playwright.sync_api import Page


class InventoryPage:
    """Страница каталога (/inventory.html) — открывается после успешного логина."""

    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, page: Page):
        self.page = page
        self.add_backpack_btn = page.locator('[data-test="add-to-cart-sauce-labs-backpack"]')
        self.add_bike_light_btn = page.locator('[data-test="add-to-cart-sauce-labs-bike-light"]')
        self.cart_badge = page.locator('.shopping_cart_badge')
        self.menu_button = page.locator('#react-burger-menu-btn')
        self.logout_link = page.locator('#logout_sidebar_link')

    def is_loaded(self) -> bool:
        return self.page.url == self.URL

    def add_backpack_to_cart(self):
        self.add_backpack_btn.click()

    def add_bike_light_to_cart(self):
        self.add_bike_light_btn.click()

    def get_cart_count(self) -> int:
        # Бейджа нет, когда корзина пуста.
        if not self.cart_badge.is_visible():
            return 0
        return int(self.cart_badge.text_content())

    def logout(self):
        self.menu_button.click()
        # FIXME: хардкод-пауза на анимацию меню. Заменить на ожидание видимости
        # logout_link (expect / wait_for), иначе тест флакает на медленной машине.
        self.page.wait_for_timeout(500)
        self.logout_link.click()
