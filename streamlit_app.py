import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

st.title("My Parents New Healthy Diner")

st.header("Breakfast Favorites")
st.text("🥣 Omega 3 & Blueberry Oatmeal")
st.text("🥗 Kale, Spinach & Rocket Smoothie")
st.text("🐔 Hard-Boiled Free-Range Egg")
st.text("🥑🍞 Avocado Toast")

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# read fruits csv file
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# picker works, but the numbers don't make any sense! We want the customer to be able to choose the fruits by name
# choose the Fruit Name Column as the Index
my_fruit_list = my_fruit_list.set_index('Fruit')

# put a pick list here so users can pick the fruit they want to include 
# pre-populate the list to set an example for the customer
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the whole fruits table on the page
# st.dataframe(my_fruit_list)

# Filter the Table Data - We'll ask our app to put the list of selected fruits into a variable called fruits_selected. 
# Then, we'll ask our app to use the fruits in our fruits_selected list to pull rows from the full data set (and assign that data to a variable called fruits_to_show). 
# Finally, we'll ask the app to use the data in fruits_to_show in the dataframe it displays on the page. 
st.dataframe(fruits_to_show)

# function to get fruityvice data
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

# new section to display FruityVice API response
st.header("Fruityvice Fruit Advice!")

# Move the Fruityvice Code into a Try-Except (with a nested If-Else)
# Introducing this structure allows us to separate the code that is loaded once from the code that should be repeated each time a new value is entered.
try:
  # user input for fruit
  fruit_choice = st.text_input("What fruit would you like information about?")
  if not fruit_choice:
    st.error("Please select a fruit to get information.")
  else:
    back_from_fxn = get_fruityvice_data(fruit_choice)
    st.dataframe(back_from_fxn)

except URLError as e:
  st.error()

# don't run anything past here while we troubleshoot
st.stop()

# # query snowflake account metadata
# my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_data_row = my_cur.fetchone()
# st.text("Hello from Snowflake:")
# st.text(my_data_row)

# query data from snowflake
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
# my_data_row = my_cur.fetchone()
my_data_row = my_cur.fetchall()
st.text("The fruit load list contains:")
st.dataframe(my_data_row)

# add fruits by user
add_my_fruit = st.text_input("What fruit would you like to add?")
my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES ('from streamlit')")
st.write("Thanks for adding " + add_my_fruit)
