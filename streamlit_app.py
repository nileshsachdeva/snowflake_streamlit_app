import streamlit as st
import pandas as pd
import requests
import snowflake.connector

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

# new section to display FruityVice API response
st.header("Fruityvice Fruit Advice!")

# user input for fruit
fruit_choice = st.text_input("What fruit would you like information about?", "Kiwi")
st.write("The user entered ", fruit_choice)

# separate the base URL from the fruit name (which will make it easier to use a variable there)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# st.text(fruityvice_response.json()) # just writes data to the screen

# normalize json 
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
st.dataframe(fruityvice_normalized)

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
my_data_row = my_cur.fetchone()
st.text("The fruit load list contains:")
st.text(my_data_row)
