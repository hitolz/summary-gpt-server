from flask import render_template

from app import creat_app
from app.extension import db
from app.models.user import User

config_name = 'development'
app = creat_app(config_name)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
