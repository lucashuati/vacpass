from celery import Celery

app = Celery()
app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tasks.add',
        'schedule': 30.0,
        'args': (16, 16)
    },
}

@app.task
def test(arg):
    return arg
