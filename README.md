# Taurus Driving School

Односторінковий сайт автошколи Taurus, об’єднаний в один навчальний вебзастосунок за результатами практичних завдань №1–4.

## Технології

- HTML5, CSS3, Flexbox, CSS Grid та адаптивні media queries для 375, 768 і 1440 px;
- Vanilla JavaScript без фреймворків: меню, тема, localStorage, відгуки, DOM та Fetch API;
- Python Flask та SQLite для приймання заявок і збереження повідомлень;
- unittest та GitHub Actions для автоматизованої перевірки.

## Запуск frontend + backend

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
py app.py
```

Відкрийте `http://127.0.0.1:5000/`. База `database.sqlite` створюється автоматично за схемою [schema.sql](./schema.sql). Адмін-сторінка: `http://127.0.0.1:5000/messages`.

Для локальної демонстрації використовуються `admin` / `change-me`. Для реального розгортання задайте `TAURUS_ADMIN_USER` і `TAURUS_ADMIN_PASSWORD` змінними середовища.

## Тести

```powershell
python -m unittest discover -s tests -v
```

CI налаштовано у `.github/workflows/tests.yml`.

## Звірка з ТЗ

- №1: семантична розмітка, 3+ секції, зображення з `alt`, посилання, форма, footer, responsive CSS.
- №2: окремий `script.js`, меню, додаткова інформація, темна тема, localStorage, HTML/JS-валідація, динамічні відгуки та додавання/видалення без перезавантаження.
- №3: POST API, серверна валідація, SQLite, параметризовані SQL-запити, авторизований список і DELETE API, Fetch API.
- №4: breakpoint-и 375/768/1440, 3 автоматизовані тести, CI workflow, `.gitignore` та інструкція запуску.

GitHub, Lighthouse-звіт, HTTPS-хостинг і ZIP-архів потребують зовнішньої публікації; локальна структура для них підготовлена.
