# ML_service
Репо для курса "практикум по созданию ML сервисов"

## Инструкция по запуску сервера
1) Создание и запуск окружения:
    
    `poetry install`

    `poetry shell`

2) Создание необходимых таблиц в БД:

    `python create_db.py`

3) Запуск сервера:

    `python run main.py` - Запуск основного сервиса
    `celery -A src.service.api.tasks.make_prediction:celery worker --loglevel=INFO` - Запуск celery для фоновых задач
    `celery -A src.service.api.tasks.make_prediction:celery flower` - Запуск сервиса мониторинга
