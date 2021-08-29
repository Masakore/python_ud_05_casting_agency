import os

# Enable debug mode.
DEBUG = True

# Connect to the database
DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_NAME = os.getenv('DB_NAME', 'test_model_agency')

SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(
    DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = False
