# Importar los paquetes necesarios
import requests
from bs4 import BeautifulSoup
import unicodedata
import pandas as pd

# Definir funciones auxiliares
def date_time(table_cells):
    """
    Esta función devuelve la fecha y hora de la celda de la tabla HTML
    """
    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]

def booster_version(table_cells):
    """
    Esta función devuelve la versión del propulsor de la celda de la tabla HTML
    """
    out = ''.join([booster_version for i, booster_version in enumerate(table_cells.strings) if i % 2 == 0][0:-1])
    return out

def landing_status(table_cells):
    """
    Esta función devuelve el estado de aterrizaje de la celda de la tabla HTML
    """
    out = [i for i in table_cells.strings][0]
    return out

def get_mass(table_cells):
    """
    Esta función devuelve la masa de la carga útil de la celda de la tabla HTML
    """
    mass = unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass:
        mass.find("kg")
        new_mass = mass[0:mass.find("kg")+2]
    else:
        new_mass = 0
    return new_mass

# URL de la página de Wikipedia
static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"

# Realizar la solicitud HTTP GET a la URL
html_data = requests.get(static_url)

# Crear un objeto BeautifulSoup a partir del contenido HTML
soup = BeautifulSoup(html_data.text, 'html.parser')

# Crear un diccionario para almacenar los datos de los lanzamientos
launch_dict = {
    'Flight No.': [],
    'Launch site': [],
    'Payload': [],
    'Payload mass': [],
    'Orbit': [],
    'Customer': [],
    'Launch outcome': [],
    'Version Booster': [],
    'Booster landing': [],
    'Date': [],
    'Time': []
}

# Extraer la tabla de lanzamientos
for table_number, table in enumerate(soup.find_all('table', "wikitable plainrowheaders collapsible")):
    for rows in table.find_all("tr"):
        if rows.th:
            if rows.th.string:
                flight_number = rows.th.string.strip()
                flag = flight_number.isdigit()
        else:
            flag = False
        row = rows.find_all('td')
        if flag:
            # Número de vuelo
            launch_dict['Flight No.'].append(flight_number)
            # Fecha y hora
            datatimelist = date_time(row[0])
            date = datatimelist[0].strip(',')
            launch_dict['Date'].append(date)
            time = datatimelist[1]
            launch_dict['Time'].append(time)
            # Versión del propulsor
            bv = booster_version(row[1])
            if not bv:
                bv = row[1].a.string
            launch_dict['Version Booster'].append(bv)
            # Sitio de lanzamiento
            launch_site = row[2].a.string
            launch_dict['Launch site'].append(launch_site)
            # Carga útil
            payload = row[3].a.string
            launch_dict['Payload'].append(payload)
            # Masa de la carga útil
            payload_mass = get_mass(row[4])
            launch_dict['Payload mass'].append(payload_mass)
            # Órbita
            orbit = row[5].a.string
            launch_dict['Orbit'].append(orbit)
            # Cliente
            if row[6].a:
                customer = row[6].a.string
            else:
                customer = None
            launch_dict['Customer'].append(customer)
            # Resultado del lanzamiento
            launch_outcome = list(row[7].strings)[0]
            launch_dict['Launch outcome'].append(launch_outcome)
            # Estado de aterrizaje del propulsor
            booster_landing = landing_status(row[8])
            launch_dict['Booster landing'].append(booster_landing)

# Crear un DataFrame a partir del diccionario
df = pd.DataFrame(launch_dict)

# Exportar los datos a un archivo CSV
df.to_csv('spacex_web_scraped.csv', index=False)

# Imprimir las primeras filas del DataFrame
print(df.head())
