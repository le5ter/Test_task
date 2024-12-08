from flask import Blueprint
from flask_restx import Api

api_v1 = Api(
    version='1.0',
    title="Flask-RESTplus Example API",
    description=("RESTful API for Test task", )
)


def init_app(app, **kwargs):
    api_v1_blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

    api_v1.init_app(api_v1_blueprint)
    app.register_blueprint(api_v1_blueprint)


