from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

routes = Blueprint('routes', __name__)

@routes.route('/register', methods = ['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
   
    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first()  :
        return jsonify({"msg": "Este usuario ya existe "}), 409
    
    user = User(username = username, email = email)      
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg":"Usuario registrado satisfactoriamente "}), 201

@routes.route('/login', methods = ['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')


    username = User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first()

    if not username or not username.check_password(password):
        return jsonify({'msg':'credenciales invalidos '}), 401
    
    access_token = create_access_token(identity = {'email': email})
    return jsonify(access_token = access_token ), 200

    

@routes.route('/profile', methods = ['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as = current_user), 200


