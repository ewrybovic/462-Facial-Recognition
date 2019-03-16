import sqlite3

conn = sqlite3.connect('FacRecDatabase.db')

c = conn.cursor()

c.execute('''CREATE TABLE FaceRecInfo (name, website)''')

conn.commit()
conn.close()
