from flask import Flask
from routes import UsersRoutes

app = Flask(__name__)


def init_app():
    app.register_blueprint(MascotasRoutes.app, url_prefix='/mascotas')
    
    return app