from .admin import admin

DEFAULT_BLUEPRINT = [
    (admin, '/'),
]


def config_blueprint(app):
    for blueprint, prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint, url_prefix=prefix)
