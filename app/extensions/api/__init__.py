from flask import current_app


def serve_swaggerui_assets(path):
    if not current_app.debug:
        import warnings
        warnings.warn(
            "/swaggerui/ is recommended to be served by public-facing server (e.g. NGINX)"
        )
    from flask import send_from_directory
    return send_from_directory('../static/', path)


def init_app(app, **kwargs):
    app.route('/swaggerui/<path:path>')(serve_swaggerui_assets)
