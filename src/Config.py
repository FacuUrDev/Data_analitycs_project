from decouple import config

class Config:
    # Configuración de la conexión a la base de datos PostgreSQL
    BASE_URL = config('BASE_URL')#se utiliza timemachine de onecall
    API_KEY = config('API_KEY')
    DB_USERNAME = config('DB_USER')
    DB_PASSWORD = config('DB_PASSWORD')
    DB_HOST = config('DB_HOST')
    DB_PORT = config('DB_PORT')
    DB_NAME = config('DB_NAME')
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"