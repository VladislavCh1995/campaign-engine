# Campaign Rule Engine

Сервис для автоматического управления статусом рекламных кампаний на основе бизнес-правил.

## Архитектура движка правил

- Каждое правило — отдельный класс, наследующий `BaseRule`.
- `RuleEngine` применяет правила по порядку приоритета.
- Добавление нового правила не требует изменения существующего кода.
- Правила тестируются изолированно, без БД.

## Технологии

- Python 3.13
- FastAPI
- SQLAlchemy 2.0
- Pydantic v2
- PostgreSQL (Docker)
- pytest

## Требования

- Python 3.13 https://www.python.org/downloads/release/python-31314/
- Docker Desktop https://www.docker.com/products/docker-desktop/
- Git (опционально)


## Установка и запуск

1. **Клонируй или распакуй архив** в папку `campaign-engine`.

2. **Запусти PostgreSQL через Docker:**
   ```bash
   docker-compose up -d
3. **Создание виртуального окружения**
python -m venv venv
venv\Scripts\activate   # Windows
# или source venv/bin/activate   # Linux/Mac
4. **Установка зависимостей**
pip install -r requirements.txt
5. **Запуск сервера**
uvicorn app.main:app --reload
6. **Открытие swagger:**
http://127.0.0.1:8000/docs
7. **Тест**
Написан unit-тест для проверки логики правила ManagementRule с использованием pytest. Тест не требует подключения к базе данных и проверяет бизнес-логику изолированно.

Что проверяется:

- Если у кампании is_managed = False — правило срабатывает, статус не меняется, возвращается management_off.
- Если is_managed = True — правило не срабатывает.

pytest tests/test_rules.py -v

Ожидаемый результат: тесты проходят успешно (PASSED).
