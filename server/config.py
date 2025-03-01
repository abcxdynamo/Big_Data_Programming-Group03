# server info
import models
from base.base_model import db
from models.user import User
from models.user_role import UserRole

SERVER_PORT = 5001
REGISTER_SERVER_NAME = "performa"

SECRET_KEY = "ABCX_PERFORMA"

DB_URI = 'mysql+pymysql://root:123456@localhost:3306/performa?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = True

# don't submit next line when set to True
FIRST_RUN = False


def init_database(_app):
    with _app.app_context():
        db.drop_all()
        db.create_all()
        UserRole.save_all(
            UserRole(id=1, name="STUDENT"),
            UserRole(id=2, name="PROFESSOR"),
            UserRole(id=3, name="ADMIN"),
        )

        User.save_all(
            User(email="cchen7166@conestogac.on.ca", first_name="Ce", last_name="Chen", role_id=1),
            User(email="mila@conestogac.on.ca", first_name="Xiaoman", last_name="Yang", role_id=1),
            User(email="hubin@conestogac.on.ca", first_name="Bin", last_name="Hu", role_id=1),
            User(email="anuroopa@conestogac.on.ca", first_name="Anuroopa", last_name="Balachandran", role_id=1),
            User(email="cchen71666@conestogac.on.ca", first_name="Jomis", last_name="X", role_id=2),
            User(email="cchen716666@conestogac.on.ca", first_name="Admin", last_name="X", role_id=3),
        )
    pass
