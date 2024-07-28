from flask import Flask
from routes import UsersRoutes

app = Flask(__name__)


def init_app():
    app.register_blueprint(UsersRoutes.app, url_prefix='/usuarios')
    
    return app