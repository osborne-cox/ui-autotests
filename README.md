# UI Autotests — saucedemo.com

[![UI Tests](https://github.com/osborne-cox/ui-autotests/actions/workflows/tests.yml/badge.svg)](https://github.com/osborne-cox/ui-autotests/actions)

Автоматизированные UI-тесты на Python + Playwright по архитектуре **Page Object Model**.

## Что тестируется

[Sauce Demo](https://www.saucedemo.com) — демо e-commerce сайт специально для QA-практики.

| Модуль | Кейсы | Покрытие |
|---|---|---|
| Авторизация | 3 | Успешный логин, неверный пароль, заблокированный аккаунт |
| Корзина | 2 | Добавление 1 и 2 товаров, проверка счётчика |
| Выход | 1 | Logout → редирект на страницу логина |

## Стек

- **Python 3.11+**
- **Playwright** — браузерная автоматизация (Chromium)
- **pytest** + **pytest-playwright** — тест-фреймворк и готовые фикстуры
- **Page Object Model** — архитектурный паттерн

## Структура проекта

```
ui-autotests/
├── pytest.ini           # конфиг pytest (pythonpath, опции запуска)
├── requirements.txt     # зависимости
├── .gitignore
├── pages/               # Page Objects — описание страниц
│   ├── login_page.py    # страница авторизации
│   └── inventory_page.py # страница каталога товаров
└── tests/               # тесты
    ├── test_login.py    # тесты авторизации
    └── test_cart.py     # тесты корзины
```

## Запуск

```bash
# Установка зависимостей
pip install -r requirements.txt
playwright install chromium

# Запуск всех тестов (по умолчанию headless — без окна браузера)
pytest

# Посмотреть, как кликает браузер
pytest --headed
```

Фикстуры `page`/`context`/`browser` берутся из `pytest-playwright` — свои не
изобретаем: меньше кода, стандартное поведение, флаг `--headed` работает из коробки.

## Ожидаемый вывод

```
tests/test_login.py::TestLogin::test_successful_login     PASSED
tests/test_login.py::TestLogin::test_login_wrong_password PASSED
tests/test_login.py::TestLogin::test_login_locked_user    PASSED
tests/test_cart.py::TestCart::test_add_one_item           PASSED
tests/test_cart.py::TestCart::test_add_two_items          PASSED
tests/test_cart.py::TestCart::test_logout                 PASSED
```

## Два архитектурных решения

**1. Page Object Model** отделяет поиск элементов от логики тестов.

```python
# Без POM — хрупко:
page.fill('#user-name', 'standard_user')  # в каждом тесте
page.click('#login-button')               # id изменится → правок столько же, сколько тестов

# С POM — устойчиво:
login_page.login('standard_user', 'secret_sauce')  # 1 метод, 1 точка правки
```

Меняется селектор — правим только Page Object, тесты не трогаем.

**2. Web-first assertions (`expect`)** вместо ручных проверок. `expect()` сам
дожидается нужного состояния с авто-ретраями, поэтому в коде нет ни `time.sleep`,
ни чтения `page.url` сразу после клика — это убирает флаки на медленных прогонах.

```python
expect(page).to_have_url(InventoryPage.URL)   # подождёт навигацию
expect(cart_badge).to_have_text("1")           # подождёт появление бейджа
```
