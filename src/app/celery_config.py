from celery import Celery, Task

def celery_init_app(app):
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app = Celery(
        app.name,
        broker='redis://localhost:6379/0',  
        backend='redis://localhost:6379/0' ,
        task_cls=FlaskTask
    )

    celery_app.config_from_object(app.config)
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    celery_app.autodiscover_tasks(['app.tasks'])
    return celery_app