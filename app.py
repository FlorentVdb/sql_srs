#pylint: disable=missing-module-docstring
import ast

import duckdb
import streamlit as st

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

#solution_df = duckdb.sql(ANSWER_STR).df()

st.write(
    """
# SQL SRS
Spaced Repetition System SQL practice
"""
)

with st.sidebar:
    theme = st.selectbox(
        "What would you like to review?",
        ("cross_joins", "GroupBy", "window_functions"),
        index=None,
        placeholder="Select a theme...",
    )
    st.write("You selected:", theme)

    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df()
    st.write(exercise)

st.header("Enter your code here: ")
query = st.text_area(label="Votre code SQL ici", key="user_input")
if query:
    result = con.execute(query).df()
    st.dataframe(result)
#
#    if len(result.columns) != len(solution_df.columns):
#        st.write("Some columns are missing")
#
#    try:
#        result = result[solution_df.columns]
#        st.dataframe(result.compare(solution_df))
#    except KeyError as e:
#        st.write("Some columns are missing")
#
#    n_lines_differences = result.shape[0] - solution_df.shape[0]
#    if n_lines_differences != 0:
#        st.write(
#            f"result has a {n_lines_differences} lines difference with the solution"
#        )
#
#
tab2, tab3 = st.tabs(["Tables", "Solution"])


with tab2:
    exercise_tables = ast.literal_eval(exercise.loc[0, "table"])
    for tab in exercise_tables:
        st.write(f"table: {tab}")
        df_table = con.execute(f"SELECT * FROM {tab}").df()
        st.dataframe(df_table)
#    st.write("table: food_item")
#    st.dataframe(food_items)
#    st.write("table: expected")
#    st.dataframe(solution_df)

with tab3:
    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()
    st.write(answer)
