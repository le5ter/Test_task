from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/swagger'
API_URL = '/api/v1/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL
)


def init_app(app, **kwargs):
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
