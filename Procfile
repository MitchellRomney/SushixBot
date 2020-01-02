release: python manage.py migrate
web: gunicorn ItsSushix.asgi:application -b 0.0.0.0:$PORT -w 4 -k uvicorn.workers.UvicornWorker
celeryworker: celery -A ItsSushix worker -l info -B --autoscale=6,3
twitchbot: python Bots/TwitchBot/bot.py