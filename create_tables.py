
import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

# MUST BE INTEGER
# This is the only place where int vs INTEGER matters—in auto-incrementing columns
create_table = "CREATE TABLE IF NOT EXISTS offers (id INTEGER PRIMARY KEY, price real, items_in_stock integer)"
cursor.execute(create_table)


create_table = "CREATE TABLE IF NOT EXISTS products (name text PRIMARY KEY, description text)"
cursor.execute(create_table)

connection.commit()

connection.close()
