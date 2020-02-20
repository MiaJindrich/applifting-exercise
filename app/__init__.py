from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apscheduler.scheduler import Scheduler


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models
from .offer_microservice import OfferMicroservice
 
sched = Scheduler()
sched.start()
 
service = OfferMicroservice(app.config['BASE_URL'])
service.fetch_data_from_api()
# sched.add_interval_job(service.fetch_data_from_api, minutes=1)

from app import routes


if __name__ == '__main__':
    app.run(debug=True)