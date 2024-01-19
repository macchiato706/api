from fastapi import FastAPI, HTTPException, Request, Response, Depends
from pydantic import BaseModel, Field, ValidationError
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import Optional
from contextlib import contextmanager
import math
import uvicorn
import sqlite3



app = FastAPI()



class Product(BaseModel):
    name: str = Field(..., max_length=8, pattern=r'^[A-Za-z]+$')
    amount: Optional[int] = 1
    price: Optional[float] = None
    #price: float

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"message": "ERROR"},
    )

def get_db_connection():
    conn = sqlite3.connect('stocks.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.post("/v1/stocks")
def create_or_update_stocks(product: Product, response: Response, conn: sqlite3.Connection = Depends(get_db_connection)):
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT amount FROM stocks WHERE name = ?', (product.name,))
        item = cursor.fetchone()
        if item:
            new_amount = item['amount'] + product.amount
            cursor.execute('UPDATE stocks SET amount = ? WHERE name = ?', (new_amount, product.name))
        else:
            cursor.execute('INSERT INTO stocks (name, amount) VALUES (?, ?)', (product.name, product.amount))
        conn.commit()
        return {"name": product.name, "amount": new_amount if item else product.amount}
    except sqlite3.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
   
    return {"name": product.name, "amount": product.amount}

@app.get("/v1/stocks/{name}")
def check_stocks(name: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT amount FROM stocks WHERE name = ?', (name,))
    item = cursor.fetchone()

    if item:
        return {name: item[0]}
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get("/v1/stocks")
def check_all_stocks():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT name, amount FROM stocks WHERE amount > 0 ORDER BY name')
    items = cursor.fetchall()
    conn.close()

    return {item[0]: item[1] for item in items}




@app.post("/v1/sales")
def sales(product: Product, response: Response):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT amount FROM stocks WHERE name = ?', (product.name,))
    stock_item = cursor.fetchone()
    if not stock_item or stock_item[0] < product.amount:
        conn.close()
        raise HTTPException(status_code=404, detail="Not enough stock or item not found")

    new_amount = stock_item[0] - product.amount
    cursor.execute('UPDATE stocks SET amount = ? WHERE name = ?', (new_amount, product.name))

    cursor.execute('INSERT INTO sales (name, amount, price) VALUES (?, ?, ?)', (product.name, product.amount, product.price))

    conn.commit()
    conn.close()
    
    return {"name": product.name, "amount": product.amount, "price": product.price}

 

@app.get("/v1/sales")
def check_sales():
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT price, amount FROM sales")
        sales_records = cursor.fetchall()
        conn.close()

        total_sales = sum(record[0] * record[1] for record in sales_records if record[0] is not None)
        total_sales = round(total_sales, 1)

        total_sales_formatted = "{:.1f}".format(total_sales) 
        return {"sales": total_sales_formatted}
    

@app.get("/v1/sales/data")
def check_all_sales():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT name, amount, price FROM sales WHERE amount > 0 ORDER BY name')
    items = cursor.fetchall()
    conn.close()

    return {item['name']: {'amount': item['amount'], 'price': item['price']} for item in items}




@app.delete("/v1/stocks_sales")
def delete_stocks_and_sales():
    conn = get_db_connection()
    conn.execute('DELETE FROM stocks')
    conn.execute('DELETE FROM sales')
    conn.commit()
    conn.close()
    return {"message": "Stocks and sales are deleted"}






