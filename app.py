import streamlit as st
import requests
import matplotlib.pyplot as plt
import os

# 環境変数からAPIのエンドポイントを取得
API_ENDPOINT = os.getenv("API_ENDPOINT", "http://127.0.0.1:8000")

st.title('EC Website API')

# 商品名の入力

with st.form("product_info"):
    st.write("### Product")
    name = st.text_input("Product Name:", "")
    amount = st.number_input("Amount:", min_value=0)
    price = st.number_input("Price:", min_value=0)
    submit_product = st.form_submit_button("Submit Product Information")
    submit_sales = st.form_submit_button("Submit Sales Information")


if submit_product:
    response = requests.post(
        f"{API_ENDPOINT}/v1/stocks",
        json={"name": name, "amount": amount}
    )
    st.text('Success to submit!')
    
if submit_sales:
    response = requests.post(
        f"{API_ENDPOINT}/v1/sales",
        json={"name": name, "amount": amount, "price": price}
    )
    if response.status_code == 200:
            st.text('Success to submit!')
    else:
        st.error(f"Failed to get stock information. Status code: {response.status_code}, Response: {response.text}")
     


# 在庫情報のセクション
st.write("## Stocks Information")
col1, col2 = st.columns(2)

with col1:
    if st.button("Get All Stock Information"):
       response = requests.get(f"{API_ENDPOINT}/v1/stocks")
    # APIレスポンスの表示
       if response.status_code == 200:
           st.json(response.json())
           data = response.json()

           # 商品名と数量をリストに格納
           products = list(data.keys())
           amounts = list(data.values())

           # グラフの作成
           fig, ax = plt.subplots()
           ax.bar(products, amounts)
           ax.set_xlabel('Stocks')
           ax.set_ylabel('Amount')
           ax.set_title('Amount of Each Product')
 
           # Streamlitにグラフを表示
           st.pyplot(fig)
       else:
           st.error(f"Failed to get stock information. Status code: {response.status_code}, Response: {response.text}")
    

with col2:
    if st.button("Get Stock Information"):
       response = requests.get(f"{API_ENDPOINT}/v1/stocks/{name}")
    # APIレスポンスの表示
       if response.status_code == 200:
          st.json(response.json())
       else:
          st.error(f"Failed to get stock information. Status code: {response.status_code}, Response: {response.text}")
 

# 販売情報のセクション
st.write("## Sales Information")
col3, col4 = st.columns(2)

with col3:
    if st.button("Get Total Sales Information"):
       response = requests.get(f"{API_ENDPOINT}/v1/sales")
       # APIレスポンスの表示
       if response.status_code == 200:
           st.json(response.json())
       else:
           st.error(f"Failed to get total sales information. Status code: {response.status_code}, Response: {response.text}")
 

with col4:
    if st.button("Get Sales Information"):
        response = requests.get(f"{API_ENDPOINT}/v1/sales/data")
        if response.status_code == 200:
            st.text(response.json())
            data = response.json()

            # 商品名、数量、価格をリストに格納
            products = [item for item in data.keys()]
            amounts = [data[item]['amount'] for item in data.keys()]
            prices = [data[item]['price'] for item in data.keys()]

            # グラフの作成
            fig, ax1 = plt.subplots()
            colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']

            # 価格の棒グラフ
            ax1.bar(products, prices, color=colors[:len(products)], alpha=0.6)
            ax1.set_xlabel('Products')
            ax1.set_ylabel('Price')
            
            # 数量の折れ線グラフ
            ax2 = ax1.twinx()
            ax2.plot(products, amounts, color='r', marker='o')
            ax2.set_ylabel('Amount')

            # グラフのタイトル
            plt.title('Amount and Price of Each Product')

            # Streamlitにグラフを表示
            st.pyplot(fig)        
        else:
            st.error(f"Failed to create/update sales information. Status code: {response.status_code}, Response: {response.text}")



st.write("## Delete Information")
# 情報のリセット
if st.button("Delete All Information"):
    response = requests.delete(f"{API_ENDPOINT}/v1/stocks_sales")

    # APIレスポンスの表示
    if response.status_code == 200:
        st.text('Success to delete!')
    else:
        st.error(f"Failed to delete information. Status code: {response.status_code}, Response: {response.text}")
        

