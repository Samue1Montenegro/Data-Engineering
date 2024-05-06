"""
Script el cual se extren datos financieros en formato JSON 
(porcentaje de rendimiento de diferentes sectores financieros),
desde la API https://financialmodelingprep.com/api/v3/sectors-performance?apikey=uuvQnt7H37YoK28LDFsj4Bor8Dn9IBuM
Se procesan los datos en un diccionario. 
Luego se expresan los datos en un Dataframe para verificar el formato requerido.
Finalmente se guardan los datos en un archivo excel para mejor visualización y verificación de datos.

"""

# Librerias utilizadas para el desarrollo del script
import requests
import pandas as pd
import os.path
from datetime import datetime


# Se define nombre del archivo Excel
file_name = "datos.xlsx"

# Verificar si el archivo existe en el directorio actual
if not os.path.isfile(file_name):
    # Si el archivo no existe, crearlo en el directorio actual
    open(file_name, "w").close()

# Obtener datos de sectores de rendimiento
sectors_url = "https://financialmodelingprep.com/api/v3/sectors-performance?apikey=uuvQnt7H37YoK28LDFsj4Bor8Dn9IBuM"
sectors_response = requests.get(sectors_url)
if sectors_response.status_code == 200:
    try:
        sectors_data = sectors_response.json()

        # Se imprime en consola para verificar datos y formato correctos.
        print(sectors_data, "\n")
        print("---" * 20, "\n")

        # Crear un diccionario para almacenar los datos, incluyendo la fecha
        data = {"Fecha": [datetime.now().strftime("%Y-%m-%d")]}

        # Iterar sobre los datos de sectores y agregarlos al diccionario
        for sector_info in sectors_data:
            sector = sector_info["sector"]
            changes_percentage = sector_info["changesPercentage"]
            data[sector] = [changes_percentage]

        # Se crea Dataframe con los datos recolectados desde la api
        df = pd.DataFrame(data)

        # Guardar DataFrame en archivo Excel
        df.to_excel(file_name, index=False, engine="openpyxl")

        # Se imprime el Dataframe en consola para control
        print(df)
    except Exception as a:
        # Mensaje que especifica que error ocurre
        print(f"Error en código:", {a})
else:
    # En caso de no obtener respuesta de la Api se imprime un mensaje
    print("Error de status en API..")


"""
Query SQL con la cual se creó la Tabla en Redshift
"""

"""
CREATE TABLE datos_financieros(
    id INT IDENTITY(1,1), -- Identificador único para cada registro
    Basic_Materials DECIMAL,
    Communication_Services DECIMAL,	
    Consumer_Cyclical DECIMAL,	
    Consumer_Defensive DECIMAL,	
    Energy DECIMAL,	
    Financial_Services DECIMAL,	
    Healthcare DECIMAL,	
    Industrials DECIMAL,	
    Real_Estate DECIMAL,	
    Technology DECIMAL,	
    Utilities DECIMAL,
    fecha_ingesta TIMESTAMP DEFAULT CURRENT_TIMESTAMP --columna temporal para el control de ingesta de datos
);

"""
