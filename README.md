# UI Autotests — saucedemo.com

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
- **pytest** — тест-фреймворк
- **Page Object Model** — архитектурный паттерн

## Структура проекта

```
ui-autotests/
├── conftest.py          # Настройка браузера и фикстуры pytest
├── requirements.txt     # Зависимости
├── pages/               # Page Objects — описание страниц
│   ├── login_page.py    # Страница авторизации
│   └── inventory_page.py # Страница каталога товаров
└── tests/               # Тесты
    ├── test_login.py    # Тесты авторизации
    └── test_cart.py     # Тесты корзины
```

## Запуск

```bash
# Установка зависимостей
pip install -r requirements.txt
playwright install chromium

# Запуск всех тестов
pytest tests/ -v

# Запуск с видимым браузером (уже включено по умолчанию)
pytest tests/ -v --headed
```

## Пример вывода

```
tests/test_login.py::TestLogin::test_successful_login    PASSED
tests/test_login.py::TestLogin::test_login_wrong_password PASSED
tests/test_login.py::TestLogin::test_login_locked_user   PASSED
tests/test_cart.py::TestCart::test_add_one_item          PASSED
tests/test_cart.py::TestCart::test_add_two_items         PASSED
tests/test_cart.py::TestCart::test_logout                PASSED

6 passed in 12.34s
```

## Архитектурное решение

**Page Object Model** отделяет логику поиска элементов от логики тестов.

```python
# Без POM — хрупко:
page.fill('#user-name', 'standard_user')  # В каждом из 10 тестов
page.click('#login-button')               # Если id изменится — 10 правок

# С POM — устойчиво:
login_page.login('standard_user', 'secret_sauce')  # 1 метод, 1 правка
```

Если разработчик меняет селектор — правим только Page Object, тесты не трогаем.
