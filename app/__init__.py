from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apscheduler.scheduler import Scheduler


def create_app(config_object=None):
    app = Flask(__name__)
    config = Config()
    if config_object is not None:
        config = config_object
    app.config.from_object(config)
    return app

def get_offer_microservice():
    service = OfferMicroservice(app.config['BASE_URL'])
    return service

app = create_app()
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models
from .offer_microservice import OfferMicroservice
 
sched = Scheduler()
sched.start()

sched.add_interval_job(get_offer_microservice().fetch_data_from_api, minutes=1)

from app import routes


if __name__ == '__main__':
    app.run(debug=True)