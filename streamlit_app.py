import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

# Title
streamlit.title('My Parents New Healthy Diner')

# Breakfast Favorites menu items
streamlit.header('🥣 Breakfast Favorites')
streamlit.text('🥗 Omega 3 & Blueberry Oatmeal')
streamlit.text('🐔 Kale, Spinach & Rocket Smoothie')
streamlit.text('🥑🍞 Hard-Boiled Free-Range Egg')

# Build your own smoothie menu items
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Fruityvice function
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.dataframe(fruits_to_show)

streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice  = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information about")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()
  
# display the information from the fruit load list
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)

# take user input and add to the fruit load list
add_my_fruit = streamlit.text_input("What fruit would you like to add?", "")
streamlit.write("Thanks for adding ", add_my_fruit)
my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from streamlit')")

