from flask import Blueprint, request, jsonify
from models import db, Notification
import requests
from circuitbreaker import circuit

routes = Blueprint('routes', __name__)

LOGIN_SERVICE_URL = "http://127.0.0.1:5000/profile"

@circuit(failure_threshold = 3, recovery_timeout = 30)
def validate_token(token):
    headers = {
    "Authorization" : token,
    }
    #print(headers)
    response = requests.get(LOGIN_SERVICE_URL, headers = headers)
    if response.status_code != 200 :
        raise Exception("Validacion de token fallida ")
    return response.json()

@routes.route('/notify', methods=['POST'])
def notify():
    token = request.headers.get('Authorization')
    try:
        user_info = validate_token(token)
        #print(user_info)
    except Exception as e:
        return jsonify({"msg":str(e)}), 503
    else:
        print(user_info['logged_in_as']['email'])
        message = "Inicio de sesion exitosa(?)"
        notification = Notification(message = message, user_email = user_info['logged_in_as']['email'])
        db.session.add(notification)
        db.session.commit()

    return jsonify({"msg": "Notificacion enviada "}), 200

@routes.route('/notifications', methods=['GET'])
def get_notifications():
    notifications = Notification.query.all()
    return jsonify([{"message": n.message, "user_email": n.user_email} for n in notifications]), 200


