import pytest
from playwright.sync_api import sync_playwright, Page, Browser

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# conftest.py — специальный файл pytest.
# pytest подхватывает его автоматически — не нужно
# импортировать вручную.
#
# Здесь живут FIXTURES — функции которые запускаются
# ДО и ПОСЛЕ тестов. Это как preCondition и postCondition
# в тест-кейсах, только в коде.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@pytest.fixture(scope="session")
def browser():
    """
    scope="session" — браузер запускается ОДИН РАЗ для всей сессии тестов.
    Это быстрее чем открывать новый браузер для каждого теста.

    yield — это как return, но с продолжением:
    1. Код ДО yield выполняется перед тестами (setup)
    2. yield отдаёт браузер тестам
    3. Код ПОСЛЕ yield выполняется после всех тестов (teardown)
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False  # False = видишь браузер во время теста
                            # True  = браузер невидимый (быстрее, для CI/CD)
        )
        yield browser       # Отдаём браузер тестам
        browser.close()     # После всех тестов — закрываем


@pytest.fixture(scope="function")
def page(browser: Browser) -> Page:
    """
    scope="function" — новая вкладка для КАЖДОГО теста.

    Зачем: если один тест залогинился, следующий не должен
    об этом знать — каждый тест независим.

    Это как принцип изоляции в тест-кейсах:
    каждый кейс начинается с чистого состояния.
    """
    context = browser.new_context()  # Новый контекст = чистые куки и сессия
    page = context.new_page()         # Новая вкладка внутри контекста
    yield page                         # Отдаём страницу тесту
    context.close()                    # После теста — закрываем контекст
