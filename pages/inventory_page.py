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

    def add_backpack_to_cart(self):
        self.add_backpack_btn.click()

    def add_bike_light_to_cart(self):
        self.add_bike_light_btn.click()

    def logout(self):
        self.menu_button.click()
        # Бургер-меню выезжает с анимацией. click() сам дожидается, пока ссылка
        # станет видимой и кликабельной (авто-ожидание Playwright), поэтому
        # хардкод-паузы здесь не нужны.
        self.logout_link.click()
