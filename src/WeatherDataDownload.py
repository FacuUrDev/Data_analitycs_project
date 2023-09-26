import csv
from datetime import datetime, timedelta
import requests
from os import makedirs
from Config import Config
from sqlalchemy import create_engine
import pandas as pd

"""
  ###
    Obtenemos datos meteorológicos de la API de OpenWeatherMap.

        Argumentos:
            url (str): URL de API para datos meteorológicos.
"""     
    
def fetch_weather_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error en la respuesta: {response.status_code}")
        return None


"""
###
    Guardamos los datos meteorológicos en un archivo CSV.

        Argumentos: 
            data (list): Lista de datos meteorológicos.
            file_path (str): Ruta del archivo CSV.
        
"""
def save_weather_data_as_csv(data, file_path):
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['city', 'date', 'temperature', 'humidity', 'wind_speed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for entry in data:
            writer.writerow(entry)

"""
# Recuperamos los datos meteorológicos de las ciudades de la API de OpenWeatherMap
# y las guardamos en un archivo CSV.   
"""
def fetch_and_save_weather_data(cityList, coordList, output_dir):
    #Indicamos las fechas de las que queremos recuperar los datos
    target_dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(1, 6)]
    all_data = []

    for i, coord in enumerate(coordList):
        city_data = {
            'city': cityList[i],
            'datos': []
        }
        #recorremos las fechas y recuperamos los datos de cada una de ellas
        for target_date in target_dates:
            url = f"{Config.BASE_URL }lat={coord['lat']}&lon={coord['lon']}&dt={int(datetime.strptime(target_date, '%Y-%m-%d').timestamp())}&appid={Config.API_KEY}&units=metric"
            response = fetch_weather_data(url)

            if response is not None and 'data' in response:
                city_data['datos'].extend(response['data'])
            else:
                print(f"Error recuperando datos de {cityList[i]} para la fecha {target_date}")
        #guardamos los datos de la ciudad en la lista de datos
        for day_data in city_data['datos']:
            all_data.append({
                'city': city_data['city'],
                'date': datetime.fromtimestamp(day_data['dt']),
                'temperature': day_data['temp'],
                'humidity': day_data['humidity'],                
                'wind_speed': day_data['wind_speed'],
            })
    #creamos el directorio de salida si no existe
    makedirs(output_dir, exist_ok=True)
    output_file_path = f'{output_dir}tiempodiario_{datetime.now().strftime("%Y%m%d")}.csv'
    save_weather_data_as_csv(all_data, output_file_path)

    print(f"Recuperación de datos y conversión a CSV completada. Datos guardados en {output_file_path}")

# Leer las credenciales de conexión a la base de datos desde el archivo config.py

config = Config()

# Función para cargar datos de CSV a la base de datos
def load_data_to_database(csv_path, database_uri):
    df = pd.read_csv(csv_path)
    engine = create_engine(database_uri)
    table_name = "weather_data"
    df.to_sql(table_name, engine, if_exists="append", index=False)
    print(f"Datos cargados en la tabla '{table_name}'.")

def load_data_into_database(csv_paths, database_uri):
    # Cargar datos de todos los archivos CSV a la base de datos
    for csv_path in csv_paths:
        load_data_to_database(csv_path, database_uri)