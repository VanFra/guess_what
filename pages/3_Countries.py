import streamlit as st
from openai import OpenAI
from Game import get_country_list

#set page header
st.title("_Guess What?_ - :rainbow[Country Edition]")
st.image("https://www.pngkit.com/png/full/81-815202_flag-banner-png.png")

st.subheader("🌎 All countries")
st.write("""
This page displays all countries in the database. If you're stuck, check out this list.
""")

if "countries" not in st.session_state:
    st.session_state.countries = get_country_list()[0]


sorted_countries = sorted(st.session_state.countries)
col1, col2 = st.columns(2)


for i, country in enumerate(sorted_countries):
    if i % 2 == 0:
        col1.markdown(f"**{country}**".upper())
    else:
        col2.markdown(f"**{country}**".upper())