

import time                          # для замера времени загрузки
from playwright.sync_api import sync_playwright


def check_title(url: str, expected: str) -> None:
    """
    Открывает url в Chromium и проверяет, что в заголовке страницы
    есть подстрока expected. Печатает заголовок и время загрузки.
    Браузер закрывается в finally - даже если что-то упадёт.
    """
    start = time.time()              # фиксируем время старта

    with sync_playwright() as p:     # запуск движка Playwright
        # headless = False - видно окно браузера (удобно для демонстрации)
        browser = p.chromium.launch(headless=False)

        try:
            page = browser.new_page()   # новая вкладка

            # networkidle - ждём, пока сеть "успокоится" (страница догрузилась)
            page.goto(url, wait_until="networkidle")

            title = page.title()        # читаем заголовок <title>
            elapsed = time.time() - start

            # Выводим метрики - удобно для отчёта/лога
            print(f"URL:          {url}")
            print(f"Заголовок:    {title!r}")
            print(f"Длина:        {len(title)} символов")
            print(f"Загрузка:     {elapsed:.2f} с")

            # Проверяем условие: если не выполнено - AssertionError
            assert expected in title, (
                f"Ожидалось {expected!r} в заголовке, получено: {title!r}"
            )
            print("Проверка:     OK")   # дошли сюда - значит assert прошёл

        finally:
            browser.close()             # закрываем браузер ВСЕГДА


# Точка входа: код выполнится только при прямом запуске файла,
if __name__ == "__main__":
    check_title("https://playwright.dev/", "Playwright")
 
# ФИО: Кутырев Егор Федерович
# Дата: 2026-11-13
# Время: 15:40
# Описание: Скрипт запускает Chromium, открывает playwright.dev,
# печатает заголовок страницы.
# сделал так , чтобы было видно как открываеться браузер
# Код выполнен без ошибок.