from celery import Celery
import config


app = Celery('worker', broker=config.BROKER_URL, include=['celery_worker'])
app.conf.update(
    result_expires=3600,
)


if __name__ == '__main__':
    app.start()