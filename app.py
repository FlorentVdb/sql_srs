import streamlit as st
import pandas as pd
import duckdb
import io

csv = '''
beverage,price
Orange juice, 2.5
Expresso,2
Tea,3
'''

beverages = pd.read_csv(io.StringIO(csv))

csv2 = '''
food_item,food_price
Cookie, 2.5
Pain au chocolat,2
Muffin,3
'''

food_items = pd.read_csv(io.StringIO(csv2))

answer = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

solution = duckdb.sql(answer).df()

st.write("""
# SQL SRS
Spaced Repetition System SQL practice
""")

with st.sidebar:
    option = st.selectbox(
        "What would you like to review?",
        ("Joins", "GroupBy", "Windows Functions"),
        index=None,
        placeholder="Select a theme...",
    )
    st.write("You selected:", option)


st.header("Enter your code here: ")
query = st.text_area(label="Votre code SQL ici", key="user_input")
if query:
    result = duckdb.sql(query).df()
    st.dataframe(result)

tab2, tab3= st.tabs(["Tables", "Solution"])


with tab2:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_item")
    st.dataframe(food_items)
    st.write("table: expected")
    st.dataframe(solution)
with tab3:
    st.write(answer)