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

Тесты и Postman (запускать после приложения, без Celery или не во время выполнения задач на Celery):
`docker compose -f docker-compose-test.yml up --build`

Включить/отключить кеширование можно в src/config.py CACHE_ENABLE = False
Включить/отключить Celery можно в src/config.py CELERY_ON = False

Выполнено задание: ** Блюда по акции.
Скидки можно применять только к блюдам. Функция cache_discounts() в файле update_admin отвечает за кэширование скидок на блюда в редис, инвалидацию кэша старых скидок, и инвалидацию кэша приложения для блюд и списка блюд.
После сохранения в кэш, этот кэш используется методом apply_discount() в services.dish, чтобы применить скидку к блюду/списку блюд. Этот метод используется геттерами в services.dish и методом get_all_with_submenu_dishes() в services.menu
