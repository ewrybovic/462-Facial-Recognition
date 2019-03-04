import sqlite3
conn = sqlite3.connect('FacRecDatabase.db')
c = conn.cursor()
for row in c.execute('SELECT * FROM FaceRecInfo ORDER BY name'):
    print (row)
conn.close()
