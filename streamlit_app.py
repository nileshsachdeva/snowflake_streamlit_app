import streamlit as st
import pandas as pd

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
st.multiselect("Pick some fruits:", list(my_fruit_list.index))

# display the whole fruits table on the page
st.dataframe(my_fruit_list)
