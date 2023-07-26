Тестовое задание для YLab_University.
Fastapi + asyncpg + PostgreSQL

Запуск проекта:

- создать сервер и базу данных в Postgresql (можно сделать это через pgAdmin), параметры БД можно найти в файле .env
- открыть директорию ylab_test
- создать виртуальное окружение:
`python -m venv venv`
- активировть его, любым способом, например:
`venv\Scripts\activate.bat`
- установить все зависимости из requirements.txt:
`pip install -r requirements.txt`
- произвести миграции базы данных:
`alembic upgrade head`
- перейти в папку src:
`cd src`
- запустить сервер из папки src проекта:
`uvicorn main:app --reload`
- сервер поднялся ♂




Тесты и результаты тестов можно найти в папке tests.

