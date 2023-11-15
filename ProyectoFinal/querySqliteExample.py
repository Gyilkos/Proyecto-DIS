import sqlite3

con = sqlite3.connect("nombreBaseDaatos.db")

cur = con.cursor()
cur.execute("CREATE TABLE Camioneta (Patente varchar(6) PRIMARY KEY,Estado INTEGER);")
con.commit()
con.close()