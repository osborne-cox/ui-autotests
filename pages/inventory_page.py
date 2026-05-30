from playwright.sync_api import Page


class InventoryPage:
    """
    Страница каталога товаров — /inventory.html
    Сюда попадаем после успешного логина.
    """

    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, page: Page):
        self.page = page

        # Кнопки добавления конкретных товаров в корзину
        # data-test — специальный атрибут для тестов, самый надёжный локатор:
        # не зависит от CSS-классов которые могут меняться при редизайне
        self.add_backpack_btn   = page.locator('[data-test="add-to-cart-sauce-labs-backpack"]')
        self.add_bike_light_btn = page.locator('[data-test="add-to-cart-sauce-labs-bike-light"]')

        # Бейдж корзины — маленький кружок с числом товаров
        # .shopping_cart_badge — по CSS-классу (начинается с точки)
        self.cart_badge = page.locator('.shopping_cart_badge')

        # Элементы меню для выхода
        self.menu_button  = page.locator('#react-burger-menu-btn')
        self.logout_link  = page.locator('#logout_sidebar_link')

    def is_loaded(self) -> bool:
        """
        Проверить что мы на странице товаров.
        Сравниваем текущий URL с ожидаемым.
        """
        return self.page.url == self.URL

    def add_backpack_to_cart(self):
        """Добавить рюкзак в корзину"""
        self.add_backpack_btn.click()

    def add_bike_light_to_cart(self):
        """Добавить велофонарик в корзину"""
        self.add_bike_light_btn.click()

    def get_cart_count(self) -> int:
        """
        Вернуть количество товаров в корзине.
        Если бейджа нет (корзина пуста) — возвращаем 0.
        """
        if not self.cart_badge.is_visible():
            return 0

        count_text = self.cart_badge.text_content()
        # text_content() возвращает строку — "1", "2" и т.д.
        return int(count_text)
        # int() конвертирует строку "1" в число 1

    def logout(self):
        """Выйти из аккаунта через бургер-меню"""
        self.menu_button.click()

        # Ждём пока откроется боковое меню (анимация ~300мс)
        self.page.wait_for_timeout(500)
        # wait_for_timeout(ms) — пауза в миллисекундах
        # 500мс = 0.5 секунды

        self.logout_link.click()
