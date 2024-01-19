import sqlite3


conn = sqlite3.connect('/Users/maiko/Desktop/myapp/stocks.db')
cursor = conn.cursor()



cursor.execute('''
    CREATE TABLE IF NOT EXISTS stocks (
        name TEXT NOT NULL,
        amount INTEGER 

    )
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
      name TEXT NOT NULL,
      amount INTEGER DEFAULT 1,
      price FLOAT CHECK (price > 0)
    )

''')


conn.commit()
conn.close()





