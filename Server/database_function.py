import sqlite3
conn = sqlite3.connect('FacRecDatabase.db')
c = conn.cursor()

data = int(input("Enter (1) to initailize db, (2) to check db (3) to delete from db:"))

if data == 1:
# initialize
   c.execute('''CREATE TABLE FaceRecInfo (name, website)''')

   conn.commit()
   conn.close()
elif data == 2:

   for row in c.execute('SELECT * FROM FaceRecInfo ORDER BY name'):
       print (row)

elif data == 3:
   print("Enter name of user to delete")
   name_ = input()
   c.execute('''DELETE FROM FaceRecInfo WHERE name=?''', (name_,))
   conn.commit()

conn.close()



