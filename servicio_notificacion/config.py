import os

class Config:
    # Clave secreta para Flask (usada en sesiones y otros temas de seguridad)
    SECRET_KEY = os.getenv('SECRET_KEY', 'defaultsecretkey')
    
    SQLALCHEMY_DATABASE_URI = ('sqlite:///Notification.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración para interactuar con el microservicio de Login
    LOGIN_SERVICE_URL = os.getenv('http://localhost:5000/')
    
    # Configuración del Circuit Breaker ( para mejorar la resiliencia)
    CIRCUIT_BREAKER_MAX_FAILURES = int(os.getenv('CIRCUIT_BREAKER_MAX_FAILURES', 3))
    CIRCUIT_BREAKER_RESET_TIMEOUT = int(os.getenv('CIRCUIT_BREAKER_RESET_TIMEOUT', 30))

