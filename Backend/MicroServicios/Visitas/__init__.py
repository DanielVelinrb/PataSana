from flask import Flask
from routes import VisitasRoutes

app = Flask(__name__)


def init_app():
    app.register_blueprint(VisitasRoutes.app, url_prefix='/visitas')
    
    return app