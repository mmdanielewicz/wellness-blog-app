# this file is used to initialize the database connection
import sqlite3

# establish connection with the database using sqlite3
connection = sqlite3.connect('database.db')

# open the schema file and execute the sql commands to create the post table
with open('schema.sql') as f:
    connection.executescript(f.read())

# establish a cursor in the connection to interact with the database
cur = connection.cursor()

# insert two values into the post table in the database
cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post', 'Content for the first post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')
            )

# commit the changes and close the communication
connection.commit()
connection.close()

