import streamlit as st
import pandas as pd

# initializing stats variables
if "total_games" not in st.session_state:
    st.session_state.total_games = 0

if "games_won" not in st.session_state:
    st.session_state.games_won = 0

if "hints_used" not in st.session_state:
    st.session_state.hints_used = []

if "guesses_used" not in st.session_state:
    st.session_state.guesses_used = []

if "guess_value" not in st.session_state:
    st.session_state.guess_value = 0

if "guess_values" not in st.session_state:
        st.session_state.guess_values = []


#set page header
st.title("_Guess What?_ - :rainbow[Country Edition]")
st.image("https://www.pngkit.com/png/full/81-815202_flag-banner-png.png")

# region Stats                    
st.subheader("📊 Game Statistics")

# TODO: 
# "Stats" page:
# The "Stats" page displays some stats about playing like the number of games played, the average number of guesses per game. 
# The "Stats" page displays a bar chart showing he number of guesses for each game
st.write(f"""
                - You have played _{st.session_state.total_games}_ games. \n
                - Of which you have won _{st.session_state.games_won}_ games. \n
                - You have used _{round(sum(st.session_state.hints_used)/len(st.session_state.hints_used),2)if len(st.session_state.hints_used) > 0 else 0}_ hints on average.  \n
                - You have used _{round(sum(st.session_state.guesses_used)/len(st.session_state.guesses_used),2) if len(st.session_state.guesses_used) > 0 else 0}_  guesses on average. \n
                """)

number_of_games = [i for i in range(1, st.session_state.total_games + 1)]

st.write(len(st.session_state.guesses_used), len(st.session_state.hints_used), len(number_of_games))
data = pd.DataFrame({"Guesses": st.session_state.guesses_used, 
                    "Hints": st.session_state.hints_used,
                    "Games": number_of_games})


st.bar_chart(data,y=["Guesses", "Hints"],x ="Games", x_label="Game", y_label="Number of Guesses", stack="layered")   

st.write(f"average quality of guesses overall: {round(sum(st.session_state.guess_values)/st.session_state.total_games, 2) if st.session_state.total_games > 0 else 0}") # add a help icon to show what makes a good guess


st.line_chart(st.session_state.guess_values)
# endregion 