
from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from routes import routes
from flask import request
import pika
import json
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(routes)

# Configuración RabbitMQ
rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
queue_name = os.getenv("RABBITMQ_QUEUE", "login_events")

def publish_event(event):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(event))
    connection.close()

# Publicar un evento cuando el usuario se registra
@app.before_request
def before_request():
    if request.endpoint == 'routes.register':
        event = {"type": "user_registered", "message": "Nuevo usuario registrado."}
        publish_event(event)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
