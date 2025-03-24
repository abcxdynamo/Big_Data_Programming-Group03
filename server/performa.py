from flask import Flask, jsonify
from flask_cors import CORS

import config
from base.base_model import db
from routes import register_routes
from services.user_service import UserService

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.DB_URI
db.init_app(app)

CORS(app, supports_credentials=True)
register_routes(app)

if __name__ == '__main__':
    print("Stage 1")
    if config.FIRST_RUN:
        config.init_database(app)
    app.run(host='0.0.0.0', debug=True, port=config.SERVER_PORT)