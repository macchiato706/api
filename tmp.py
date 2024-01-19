import sqlite3

# 新しいデータベースファイルの作成
conn = sqlite3.connect('/Users/maiko/Desktop/AWS/stocks.db')
cursor = conn.cursor()

# 在庫テーブルの作成
cursor.execute('''
    CREATE TABLE IF NOT EXISTS stocks (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        amount INTEGER NOT NULL

    )
''')

# 売上テーブルの作成
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY,
    
        total_sales INTEGER NOT NULL

    )
''')

# 売上テーブルの初期化
cursor.execute('INSERT INTO sales (total_sales) VALUES (0)')

# 変更をコミットし、接続を閉じる
conn.commit()
conn.close()
