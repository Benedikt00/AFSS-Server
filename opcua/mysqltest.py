import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  username="root",
  password="112358",
  database="test_db_bauteile"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT posi FROM bauteile WHERE name = 'M5x20';")

for x in mycursor.fetchall():
  dt = str(x)
  print(dt)

#print(mycursor.fetchall())