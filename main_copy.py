from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, constr
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import uvicorn
import sqlite3

app = FastAPI()



class Product(BaseModel):
    name: str
    amount: int


def get_db_connection():
    conn = sqlite3.connect('stocks.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.post("/v1/stocks/")
def create_or_update_stocks(product: Product):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT amount FROM stocks WHERE name = ?', (product.name,))
    item = cursor.fetchone()
    if item:
        new_amount = item['amount'] + product.amount
        cursor.execute('UPDATE stocks SET amount = ? WHERE name = ?', (new_amount, product.name))
    else:
        cursor.execute('INSERT INTO stocks (name, amount) VALUES (?, ?)', (product.name, product.amount))
    conn.commit()
    conn.close()
    return {"name": product.name, "amount": product.amount}

@app.get("/v1/stocks/{name}")
def check_stocks(name: str):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM stocks WHERE name = ?', (name,)).fetchone()
    conn.close()
    if item:
        return {"name": name, "amount": item['amount']}
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/v1/stocks/")
def check_all_stocks():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM stocks').fetchall()
    conn.close()
    return [{"name": item['name'], "amount": item['amount']} for item in items]

@app.post("/v1/sales/")
def sales(product: Product):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT amount FROM stocks WHERE name = ?', (product.name,))
    item = cursor.fetchone()
    if item and item['amount'] >= product.amount:
        new_amount = item['amount'] - product.amount
        cursor.execute('UPDATE stocks SET amount = ? WHERE name = ?', (new_amount, product.name))
        cursor.execute('UPDATE sales SET total_sales = total_sales + ?', (product.amount,))
    else:
        conn.close()
        raise HTTPException(status_code=404, detail="Not enough stocks or item not found")
    conn.commit()
    conn.close()
    return {"name": product.name, "amount": product.amount}

@app.get("/v1/sales/")
def check_sales():
    conn = get_db_connection()
    total_sales = conn.execute('SELECT total_sales FROM sales').fetchone()
    conn.close()
    return {"total_sales": total_sales['total_sales'] if total_sales else 0}

@app.delete("/v1/stocks/")
def delete_stocks_and_sales():
    conn = get_db_connection()
    conn.execute('DELETE FROM stocks')
    conn.execute('UPDATE sales SET total_sales = 0')
    conn.commit()
    conn.close()
    return {"message": "Stocks and sales are deleted"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"message": "ERROR"},
    )



