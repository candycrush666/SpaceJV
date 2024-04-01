import psycopg2
import pandas as pd

# Establecer conexión con la base de datos PostgreSQL
conn = psycopg2.connect(
    host='localhost',
    database='postgres',
    user='postgres',
    password='chuksoo',
    port='5432'
)

# Función para ejecutar consultas y devolver un DataFrame de pandas
def execute_query(query):
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=columns)
    return df

# Tareas

# Tarea 1
task_1 = '''
        SELECT DISTINCT LaunchSite 
        FROM SpaceX
'''
print("Task 1:")
print(execute_query(task_1))
print()

# Tarea 2
task_2 = '''
        SELECT *
        FROM SpaceX
        WHERE LaunchSite LIKE 'CCA%'
        LIMIT 5
        '''
print("Task 2:")
print(execute_query(task_2))
print()

# Tarea 3
task_3 = '''
        SELECT SUM(PayloadMassKG) AS Total_PayloadMass
        FROM SpaceX
        WHERE Customer LIKE 'NASA (CRS)'
        '''
print("Task 3:")
print(execute_query(task_3))
print()

# Tarea 4
task_4 = '''
        SELECT AVG(PayloadMassKG) AS Avg_PayloadMass
        FROM SpaceX
        WHERE BoosterVersion = 'F9 v1.1'
        '''
print("Task 4:")
print(execute_query(task_4))
print()

# Tarea 5
task_5 = '''
        SELECT MIN(Date) AS FirstSuccessfull_landing_date
        FROM SpaceX
        WHERE LandingOutcome LIKE 'Success (ground pad)'
        '''
print("Task 5:")
print(execute_query(task_5))
print()

# Tarea 6
task_6 = '''
        SELECT BoosterVersion
        FROM SpaceX
        WHERE LandingOutcome = 'Success (drone ship)'
            AND PayloadMassKG > 4000 
            AND PayloadMassKG < 6000
        '''
print("Task 6:")
print(execute_query(task_6))
print()

# Tarea 7
task_7a = '''
        SELECT COUNT(MissionOutcome) AS SuccessOutcome
        FROM SpaceX
        WHERE MissionOutcome LIKE 'Success%'
        '''

task_7b = '''
        SELECT COUNT(MissionOutcome) AS FailureOutcome
        FROM SpaceX
        WHERE MissionOutcome LIKE 'Failure%'
        '''
print("Task 7:")
print("The total number of successful mission outcome is:")
print(execute_query(task_7a))
print()
print("The total number of failed mission outcome is:")
print(execute_query(task_7b))
print()

# Tarea 8
task_8 = '''
        SELECT BoosterVersion, PayloadMassKG
        FROM SpaceX
        WHERE PayloadMassKG = (
                                SELECT MAX(PayloadMassKG)
                                FROM SpaceX
                                )
        ORDER BY BoosterVersion
        '''
print("Task 8:")
print(execute_query(task_8))
print()

# Tarea 9
task_9 = '''
        SELECT BoosterVersion, LaunchSite, LandingOutcome
        FROM SpaceX
        WHERE LandingOutcome LIKE 'Failure (drone ship)'
            AND Date BETWEEN '2015-01-01' AND '2015-12-31'
        '''
print("Task 9:")
print(execute_query(task_9))
print()

# Tarea 10
task_10 = '''
        SELECT LandingOutcome, COUNT(LandingOutcome)
        FROM SpaceX
        WHERE DATE BETWEEN '2010-06-04' AND '2017-03-20'
        GROUP BY LandingOutcome
        ORDER BY COUNT(LandingOutcome) DESC
        '''
print("Task 10:")
print(execute_query(task_10))

# Cerrar conexión
conn.close()
