import streamlit as st
import requests
import os

# 環境変数からAPIのエンドポイントを取得
API_ENDPOINT = os.getenv("API_ENDPOINT", "http://127.0.0.1:8000")

st.title('EC website API')

# 商品名の入力
name = st.text_input("Enter the product name:", "")

# 量の入力
amount = st.number_input("Enter the amount:", min_value=0)

#価格の入力
price = st.number_input("Enter the price:", min_value=0)

col1, col2, col3 = st.columns(3)
with col1:
# POSTリクエストを送信するボタン
 if st.button("Create or Update Product"):
    response = requests.post(
        f"{API_ENDPOINT}/v1/stocks",
        json={"name": name, "amount": amount}
    )

    # APIレスポンスの表示
    if response.status_code == 200:
        st.success("Product created/updated successfully!")
        st.text(response.json())
    else:
        st.error(f"Failed to create/update product. Status code: {response.status_code}, Response: {response.text}")

with col2:
#全ての在庫情報を取得するボタン
 if st.button("Get All Stock Information"):
    response = requests.get(f"{API_ENDPOINT}/v1/stocks")

    # APIレスポンスの表示
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error(f"Failed to get stock information. Status code: {response.status_code}, Response: {response.text}")
        
        
with col3:
# 在庫情報を取得するボタン
 if st.button("Get Stock Information"):
    response = requests.get(f"{API_ENDPOINT}/v1/stocks/{name}")

    # APIレスポンスの表示
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error(f"Failed to get stock information. Status code: {response.status_code}, Response: {response.text}")
        
with col1:
# POSTリクエストを送信するボタン
 if st.button("Create or Update Sales"):
    response = requests.post(
        f"{API_ENDPOINT}/v1/sales",
        json={"name": name, "amount": amount, "price": price}
    )

    # APIレスポンスの表示
    if response.status_code == 200:
        st.success("Sales Information created/updated successfully!")
        st.text(response.json())
    else:
        st.error(f"Failed to create/update sales information. Status code: {response.status_code}, Response: {response.text}")

with col2:
#販売情報を取得するボタン
 if st.button("Get Sales Information"):
    response = requests.get(f"{API_ENDPOINT}/v1/sales/data")

    # APIレスポンスの表示
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error(f"Failed to get sales information. Status code: {response.status_code}, Response: {response.text}")

with col3:
#全ての販売情報を取得するボタン
 if st.button("Get Total Sales Information"):
    response = requests.get(f"{API_ENDPOINT}/v1/sales")

    # APIレスポンスの表示
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error(f"Failed to get total sales information. Status code: {response.status_code}, Response: {response.text}")
        
with col1:
#情報をリセットするボタン
 if st.button("Delete All Information"):
    response = requests.delete(f"{API_ENDPOINT}/v1/stocks_sales")

    # APIレスポンスの表示
    if response.status_code == 200:
        st.text('Success to delete!')
    else:
        st.error(f"Failed to delete information. Status code: {response.status_code}, Response: {response.text}")