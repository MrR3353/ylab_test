# Тестовое задание для YLab_University.

Стек:
* Fastapi
* asyncpg
* PostgreSQL
* Docker Compose
* Redis
* Celery + RabbitMQ

### **Запуск проекта:**

Приложение, БД, Celery, Redis:
`docker compose up --build`

Тесты (запускать после приложения с БД):
`docker compose -f docker-compose-test.yml up --build`

Включить/отключить кеширование и можно в src/config.py
