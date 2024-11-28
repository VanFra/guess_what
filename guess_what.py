import streamlit as st
from openai import OpenAI
import requests
import random 
import re

# region function defintions
# Get a list of all countries
def get_country_list():
    response = requests.get("https://restcountries.com/v3.1/all?fields=name,region,subregion")
    countries_data = response.json()
    countries = [country['name']['common'].lower() for country in countries_data]

    return countries, countries_data

# generates five hints for the country and store them in a list
def get_country_hint(country):
    prompt = f"Provide five short common fact about the country '{country}' that do not explicitly reveal its name but gives clues about it. Provide the hints in a list format where guessing the country gets gradually easier. No political references."
    
    response = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[{"role": "user", "content": prompt}]
    )
    hint = response.choices[0].message.content
    # splits the hints
    st.session_state.hints = re.split(r'\n\d+\.\s', hint)
    st.session_state.hints = [h.strip() for h in st.session_state.hints if h.strip()]

    return st.session_state.hints

def save_stats():
    st.session_state.hints_used.append(st.session_state.hint_counter)
    st.session_state.guesses_used.append(5-st.session_state.guesses_left)
    st.session_state.guess_values.append(st.session_state.guess_value)

def reset_counters():
    st.session_state.guesses_left = 5
    st.session_state.hint_counter = 0
    st.session_state.guess_value = 0

def evaluate_guess(prompt):
    for country in st.session_state.countries:
        if country.lower() in prompt.lower():  # Case insensitive match
            guessed_country = country
            break 

    # get the regions for the guess and the target respectively        
    for country in st.session_state.countries_data:
        if country['name']['common'].lower() == guessed_country.lower():
            region_guess = country["region"]
            subregion_guess = country["subregion"]
        
        if country['name']['common'].lower() == st.session_state.random_country.lower():
            region_target = country["region"]
            subregion_target = country["subregion"]
    
    # compare the regions and let the user know if they are close
    if subregion_guess == subregion_target:
        st.session_state.guess_value = st.session_state.guess_value + 1
        st.write(f"Excellent guess! Almost there!")
    elif region_guess == region_target:
        st.write(f"Good guess! The region is correct!")
        st.session_state.guess_value = st.session_state.guess_value + 2
# endregion

# region Initialization
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "start_button" not in st.session_state:
    st.session_state.start_button = None
if "messages" not in st.session_state:
    st.session_state.messages = []

if "game_running" not in st.session_state:
    st.session_state.game_running = False

if "random_country" not in st.session_state:
    st.session_state.random_country = ""
    
if "guesses_left" not in st.session_state:
    st.session_state.guesses_left = 5

if "countries" not in st.session_state:
    st.session_state.countries = get_country_list()[0]

if "countries_data" not in st.session_state:
    st.session_state.countries_data = get_country_list()[1]

if "hints" not in st.session_state:
    st.session_state.hints = []

if "hint_counter" not in st.session_state:
    st.session_state.hint_counter = 0

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


# Set page config	
st.set_page_config(page_title="Guess What - Country Edition",page_icon=":material/globe:")

#set page header
st.title("_Guess What?_ - :rainbow[Country Edition]")
st.image("https://www.pngkit.com/png/full/81-815202_flag-banner-png.png")


st.write("""Do you want to play a game? I'll choose a country and you have to guess correctly within five guesses. 
        You also have 5 hints. Let's play!""")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if st.session_state.game_running == False:
    st.write("To start the game, click the button below.")

    if st.session_state.total_games == 0:
        st.session_state.start_button = st.button("Play")
    else:
        st.session_state.start_button = st.button("Play again")
    st.session_state.messages.clear()



    if st.session_state.start_button:
        # Generate a random country
        reset_counters()
        st.session_state.total_games += 1
        st.session_state.random_country = random.choice(st.session_state.countries)
        st.write("Random Country",st.session_state.random_country)
        st.session_state.hints = get_country_hint(st.session_state.random_country)
        st.session_state.game_running = True

        with st.chat_message("assistant"):
            st.markdown("I've chosen a country. Can you guess it?")
        st.session_state.messages.append({"role": "assistant", "content": f"I've chosen a country. Can you guess it?"})
        

if st.session_state.game_running == True:
    
    if prompt := st.chat_input("Guess the country or ask for a hint!", key= f"guess_input"):
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
    
        # check whether the guess was correct
        if st.session_state.random_country.lower() in prompt.lower():
                with st.chat_message("assistant"):
                    st.markdown(f"🎉 Correct! The country was {st.session_state.random_country}.")
                st.session_state.messages.append({"role": "assistant", "content": f"🎉 Correct! The country was {st.session_state.random_country}."})
                st.session_state.games_won += 1
                st.session_state.guesses_left -= 1
                save_stats()
                st.session_state.game_running = False
                

    # check whether the user wants a hint
        elif "hint" in  prompt.lower():
            if st.session_state.hint_counter < 5:
                with st.chat_message("assistant"):
                    st.markdown(st.session_state.hints[st.session_state.hint_counter])
                st.session_state.messages.append({"role": "assistant", "content": st.session_state.hints[st.session_state.hint_counter]})
                st.session_state.hint_counter += 1
            else:
                with st.chat_message("assistant"):
                    st.markdown("You are out of hints!")
    
        # if no country is mentioned
        elif not any(country in prompt.lower() for country in st.session_state.countries):
            with st.chat_message("assistant"):
                st.markdown("Please enter a valid country name. If you are unsure of spelling you can check the list of countries.")
            st.session_state.messages.append({"role": "assistant", "content": "Please enter a valid country name."})
    
        # if the guess was wrong
        else:
            evaluate_guess(prompt)
            st.session_state.guesses_left -= 1
            # but there are still guesses left
            if st.session_state.guesses_left > 0:
                with st.chat_message("assistant"):
                    st.markdown(f"❌ Wrong! You have {st.session_state.guesses_left} guesses left.")
                st.session_state.messages.append({"role": "assistant", "content": f"❌ Wrong! You have {st.session_state.guesses_left} guesses left."})
            # no guesses left -> game over
            else:
                with st.chat_message("assistant"):
                    st.markdown(f"Game over! The country was {st.session_state.random_country}.")
                st.session_state.messages.append({"role": "assistant", "content": f"Game over! The country was {st.session_state.random_country}."})
                save_stats()
                st.session_state.game_running = False 
                
# endregion
