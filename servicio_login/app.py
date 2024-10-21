from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db
from routes import routes

app = Flask(__name__)
app.Config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(routes)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)