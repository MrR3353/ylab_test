# Тестовое задание для YLab_University.

Стек:
* Fastapi
* asyncpg
* PostgreSQL
* Docker Compose
* Redis

### **Запуск проекта:**

Приложение + БД:
`docker compose up --build`

Тесты (запускать после приложения с БД):
`docker compose -f docker-compose-test.yml up --build`

Включить/отключить кеширование и изменить параметры для запуска на Docker/localhost можно в src/config.py
