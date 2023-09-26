from WeatherDataDownload import fetch_and_save_weather_data
from WeatherDataDownload import load_data_into_database
from Config import  Config

cityList = ["London", "New York", "Cordoba", "Taipei", "Buenos Aires", "Mexico DF", "Dublin", "Tilfis", "Bogota", "Tokio"]
coordList = [{"lat": 51.5074, "lon": -0.1278}, {"lat": 40.7128, "lon": -74.0060}, {"lat": -31.4167, "lon": -64.1833}, {"lat": 25.0330, "lon": 121.5654}, {"lat": -34.6037, "lon": -58.3816}, {"lat": 19.4326, "lon": -99.1332}, {"lat": 53.3498, "lon": -6.2603}, {"lat": 41.9028, "lon": 12.4964}, {"lat": 4.7110, "lon": -74.0721}, {"lat": 35.6895, "lon": 139.6917}]
output_dir = 'data_analytics/openweather/'

fetch_and_save_weather_data(cityList, coordList, output_dir)

# Define the database URI from your config
database_uri = Config.SQLALCHEMY_DATABASE_URI

# List of CSV file paths
csv_paths = ["data_analytics/openweather/tiempodiario_20230926.csv"]#replace with your own csv file path

# Load data from CSV files into the database
load_data_into_database(csv_paths, database_uri)