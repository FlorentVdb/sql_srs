# pylint: disable=missing-module-docstring
import ast

import os
import logging
from datetime import date, timedelta

import duckdb
import streamlit as st

if "data" not in os.listdir():
    logging.error(os.listdir())
    logging.debug("creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)


def check_users_solution(user_query: str) -> None:
    """
    Check that user SQL query is correct by checking:
    1 : checking the columns
    2 : checking the values
    :param user_query: str containing the query inserted by the user
    """
    result = con.execute(user_query).df()
    st.dataframe(result)
    if len(result.columns) != len(solution_df.columns):
        st.write("Some columns are missing")
    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
        if result.compare(solution_df).shape == (0, 0):
            st.balloons()
            st.write("Correct !")
    except KeyError as e:
        st.write("Some columns are missing")
    n_lines_differences = result.shape[0] - solution_df.shape[0]
    if n_lines_differences != 0:
        st.write(
            f"result has a {n_lines_differences} lines difference with the solution"
        )


st.write(
    """
# SQL SRS
Spaced Repetition System SQL practice
"""
)

with st.sidebar:
    available_themes_df = con.execute("SELECT theme from memory_state").df()
    theme = st.selectbox(
        "What would you like to review?",
        available_themes_df["theme"].unique(),
        index=None,
        placeholder="Select a theme...",
    )
    if theme:
        st.write("You selected:", theme)
        select_exercise_query = f"SELECT * FROM memory_state WHERE theme = '{theme}'"
    else:
        select_exercise_query = f"SELECT * FROM memory_state"

    exercise = (
        con.execute(select_exercise_query)
        .df()
        .sort_values("last_reviewed")
        .reset_index(drop=True)
    )
    st.write(exercise)

    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()

solution_df = con.execute(answer).df()


st.header("Enter your code here: ")
query = st.text_area(label="Votre code SQL ici", key="user_input")

if query:
    check_users_solution(query)

for n_days in (2, 7, 21):
    if st.button(f"Revoir dans {n_days} jours"):
        next_review = date.today() + timedelta(days=n_days)
        con.execute(
            f"UPDATE memory_state SET last_reviewed = '{next_review}' WHERE exercise_name = '{exercise_name}'"
        )
        st.rerun()

if st.button("Reset"):
    con.execute(f"UPDATE memory_state SET last_reviewed = '1970-01-01'")
    st.rerun()

tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    exercise_tables = exercise.loc[0, "table"]
    for tab in exercise_tables:
        st.write(f"table: {tab}")
        df_table = con.execute(f"SELECT * FROM {tab}").df()
        st.dataframe(df_table)
#    st.write("table: food_item")
#    st.dataframe(food_items)
#    st.write("table: expected")
#    st.dataframe(solution_df)

with tab3:
    st.write(answer)
