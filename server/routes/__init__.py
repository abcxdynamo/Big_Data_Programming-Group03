from flask import Flask

from .index_bp import index_bp
from .user_bp import user_bp
from .course_bp import course_bp


def register_routes(app: Flask):
    """ register all blueprints """
    app.register_blueprint(index_bp, url_prefix="/api")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(course_bp, url_prefix="/api")
    pass