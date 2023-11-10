import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="proyectointegracion",
  port="3308"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM vehiculo")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)