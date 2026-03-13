import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Smart Cafe")

st.title("☕ Smart Cafe Ordering System")

menu = {
    "Cappuccino":120,
    "Latte":140,
    "Espresso":100,
    "Veg Sandwich":150,
    "Burger":180,
    "Brownie":100
}

cart = []

st.header("Menu")

item = st.selectbox("Choose an item", list(menu.keys()))
quantity = st.number_input("Quantity", 1, 10)

if st.button("Add to Cart"):
    cart.append((item, quantity, menu[item]*quantity))
    st.success("Item added to cart")

if len(cart) > 0:

    df = pd.DataFrame(cart, columns=["Item","Qty","Price"])
    st.table(df)

    total = df["Price"].sum()

    st.subheader(f"Total Bill: ₹{total}")

    name = st.text_input("Customer Name")
    table = st.number_input("Table Number", 1, 20)

    if st.button("Place Order"):

        order = pd.DataFrame({
            "Customer":[name],
            "Table":[table],
            "Total":[total]
        })

        if os.path.exists("orders.csv"):
            order.to_csv("orders.csv", mode="a", header=False, index=False)
        else:
            order.to_csv("orders.csv", index=False)

        st.success("Order placed successfully!")