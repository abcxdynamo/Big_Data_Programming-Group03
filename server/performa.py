import os

from flask import Flask, jsonify
from flask_cors import CORS

import config
from base.base_model import db
from routes import register_routes
from services.user_service import UserService
from task import start_scheduler

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.DB_URI
db.init_app(app)

CORS(app, supports_credentials=True)
register_routes(app)

if __name__ == '__main__':
    if config.FIRST_RUN:
        # config.init_database(app)
        pass
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or os.environ.get("FLASK_ENV") != "development":
        start_scheduler()
    app.run(host='0.0.0.0', debug=False, port=config.SERVER_PORT)