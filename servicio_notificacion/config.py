import os

class Config:
    # Clave secreta para Flask (usada en sesiones y otros aspectos de seguridad)
    SECRET_KEY = os.getenv('SECRET_KEY', 'defaultsecretkey')
    
    # Configuración de la base de datos Postgres
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/notification_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración para interactuar con el microservicio de Login
    LOGIN_SERVICE_URL = os.getenv('LOGIN_SERVICE_URL', 'http://localhost:5000/profile')
    
    # Configuración del Circuit Breaker (opcional para mejorar la resiliencia)
    CIRCUIT_BREAKER_MAX_FAILURES = int(os.getenv('CIRCUIT_BREAKER_MAX_FAILURES', 3))
    CIRCUIT_BREAKER_RESET_TIMEOUT = int(os.getenv('CIRCUIT_BREAKER_RESET_TIMEOUT', 30))

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)
