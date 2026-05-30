from playwright.sync_api import Page

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE OBJECT MODEL (POM) — главная концепция файла
#
# Этот класс описывает страницу логина:
# — ГДЕ находятся элементы (локаторы)
# — ЧТО можно с ними сделать (методы)
#
# Тесты не знают про '#user-name' или '#login-button'.
# Они просто вызывают login_page.login(user, password).
# Если разработчик поменяет id кнопки — правим ЗДЕСЬ,
# а не в каждом из 10 тестов.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class LoginPage:
    """Страница авторизации saucedemo.com"""

    URL = "https://www.saucedemo.com"

    def __init__(self, page: Page):
        """
        __init__ вызывается когда создаём объект: LoginPage(page)
        Сохраняем page чтобы использовать в методах через self.page
        """
        self.page = page

        # ЛОКАТОРЫ — способ найти элемент на странице
        # page.locator(selector) — ищет по CSS-селектору
        # '#user-name'       → элемент с атрибутом id="user-name"
        # '#password'        → элемент с id="password"
        # '#login-button'    → элемент с id="login-button"
        # [data-test="..."]  → элемент с data-атрибутом (лучший вариант)
        self.username_input = page.locator('#user-name')
        self.password_input = page.locator('#password')
        self.login_button   = page.locator('#login-button')
        self.error_message  = page.locator('[data-test="error"]')

    def open(self):
        """Открыть страницу логина в браузере"""
        self.page.goto(self.URL)
        # goto() — навигация на URL, аналог "вбить адрес в строку браузера"

    def login(self, username: str, password: str):
        """
        Ввести логин и пароль, нажать кнопку входа.

        :param username: имя пользователя
        :param password: пароль
        """
        self.username_input.fill(username)
        # fill() — очищает поле и вводит текст
        # Не используем type() — fill() надёжнее для тестов

        self.password_input.fill(password)
        self.login_button.click()
        # click() — клик мышью по элементу

    def get_error_text(self) -> str:
        """Вернуть текст сообщения об ошибке"""
        return self.error_message.text_content()
        # text_content() — возвращает текстовое содержимое элемента

    def is_error_visible(self) -> bool:
        """Проверить что ошибка видна на странице"""
        return self.error_message.is_visible()
        # is_visible() → True если элемент виден, False если скрыт
