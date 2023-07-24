Запуск проекта:

- создать базу данных в Postgresql, параметры БД можно найти в файле .env
- установить все зависимости из requirements.txt
- произвести миграции базы данных:
`alembic upgrade head`
- запустить сервер из папки src проекта:
`uvicorn main:app --reload`
- сервер поднялся ♂




