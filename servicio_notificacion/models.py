from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    message = db.Column(db.String(256), nullable = False)
    user_email = db.Column(db.String(120), nullable = False)
    timestamp = db.Column(db.DataTime, default = db.func.current_timestamp())
    