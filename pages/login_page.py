from playwright.sync_api import Page


class LoginPage:
    """Страница авторизации saucedemo.com (Page Object)."""

    URL = "https://www.saucedemo.com"

    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator('#user-name')
        self.password_input = page.locator('#password')
        self.login_button = page.locator('#login-button')
        # Локатор по data-test, а не по CSS-классу: data-test добавляют под тесты,
        # он устойчивее к редизайну.
        self.error_message = page.locator('[data-test="error"]')

    def open(self):
        self.page.goto(self.URL)

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
