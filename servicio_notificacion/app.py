from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db
from routes import routes
import pika
import os
from datetime import time
import threading

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
app.register_blueprint(routes)

# Configuración RabbitMQ
rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
queue_name = os.getenv("RABBITMQ_QUEUE", "login_events")

def consume_events():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
            channel = connection.channel()
            channel.queue_declare(queue=queue_name)

            def callback(body):
                print(f"Evento recibido: {body}")

            channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
            print("Esperando eventos...")
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError:
            print("Conexión a RabbitMQ fallida, reintentando en 5 segundos...")
            time.sleep(5)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    
    # Crear un hilo para consumir eventos de RabbitMQ
    threading.Thread(target=consume_events, daemon=True).start()
    
    # Iniciar la aplicación Flask
    app.run(debug=True, port=5001)
