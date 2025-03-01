from flask import Flask

from .index import index_bp
from .students import students_bp


def register_routes(app: Flask):
    """ register all blueprints """
    app.register_blueprint(index_bp, url_prefix="/api")
    app.register_blueprint(students_bp, url_prefix="/api/students")
    pass