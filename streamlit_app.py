import streamlit as st
import pandas as pd
import requests

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
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response.json())
