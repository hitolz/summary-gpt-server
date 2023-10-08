from flask import Blueprint


admin = Blueprint('admin', __name__)

@admin.route('/', methods=['GET'])
def index():
    return 'Hello, admin!'