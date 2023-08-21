import mysql.connector 

database = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'aungpyaesoeaps321'

)

#prepare cursor object

cursorObj = database.cursor()

#create a database
cursorObj.execute("CREATE DATABASE YouthAcademy")

print('Database created')
