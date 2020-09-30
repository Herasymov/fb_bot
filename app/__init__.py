from flask import Flask
from pymessenger2.bot import Bot, NotificationType
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config, ACCESS_TOKEN

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class OverridesBot(Bot):
    """
    Overrides class bot and fix bag
    """

    def send_recipient(self,
                       recipient_id,
                       payload,
                       notification_type=NotificationType.regular):
        payload['recipient'] = {'id': recipient_id}
        payload['notification_type'] = notification_type.value
        return self.send_raw(payload)


bot = OverridesBot(ACCESS_TOKEN)

from app import routes, models
