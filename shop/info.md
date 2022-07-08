eventlet - брокер для celery

Вдруг у кого-то Celery принимает но не обрабатывает таски (нет поддержки на Windows)
Решение:
    pip install eventlet

    celery -A <mymodule> worker -l info -P eventlet