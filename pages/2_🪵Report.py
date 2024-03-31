import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("Report")

# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read(worksheet="Vendors", usecols=list(range(6)), ttl=5)

st.dataframe(data)

st.subheader("Inventory Health Check 📦")
sql = '''

SELECT "CompanyName",
        "BusinessType",
        "YearsInBusiness",
        "AdditionalInfo",
        "OnBoardingDate"
FROM 
    Vendors
WHERE
    "status" = 1
ORDER BY
    "CompanyName" DESC;
'''

url = "https://docs.google.com/spreadsheets/d/11d8G0hsw55nF24VYe59fqNc-AyDYjjIhLJlnAKVb3V0"

df_inventory_health = conn.query(sql=sql)
st.dataframe(df_inventory_health)

st.divider()


def create_orders_dataframe():
    return pd.DataFrame({
        'OrderID': [101, 102, 103, 104],
        'CustomerName': ['CustA', 'CustB', 'CustC', 'CustD'],
        'ProductList': ['ProductA', 'ProductB', 'ProductC', 'ProductD'],
        'TotalPrice': [100, 150, 200, 250],
        'OrderDate': ['2023-8-9', '2022-9-1', '2024-1-23', '2021-9-8']
    })


orders = create_orders_dataframe()
updated_orders = orders.copy()
updated_orders['TotalPrice'] = updated_orders['TotalPrice'] * 100

st.write("CRUD Operation:")

if st.button("new worksheet"):
    conn.create(worksheet="Orders", data=orders)
    st.success("worksheet created 🎉")

if st.button("calculate total order sum"):
    sql = 'SELECT SUM("TotalPrice") as "TotalOrdersPrice" FROM Orders;'
    total_orders = conn.query(sql=sql, ttl=5)
    st.dataframe(total_orders)

if st.button("update worksheet"):
    conn.update(worksheet="Orders", data=updated_orders)
    st.success("worksheet updated 😎")

if st.button("Clear worksheet"):
    conn.clear(worksheet="Orders")
    st.success("worksheet cleared 🗑️")
