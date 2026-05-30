import pytest
from playwright.sync_api import sync_playwright, Browser, Page

# conftest.py — фикстуры pytest подхватывает отсюда автоматически.


@pytest.fixture(scope="session")
def browser():
    # Один браузер на весь прогон — быстрее, чем поднимать заново на каждый тест.
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser: Browser) -> Page:
    # Новый контекст на каждый тест → чистые куки и сессия, тесты не влияют друг на друга.
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
