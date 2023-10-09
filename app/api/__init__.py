from .ai_summary import ai_summary

DEFAULT_BLUEPRINT = [
    (ai_summary, '/'),
]


def config_blueprint(app):
    for blueprint, prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint, url_prefix=prefix)
