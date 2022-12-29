import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")



streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#Set the picker to choose from the Fruit column not the UID column
#Fruit column became the UID for the table
my_fruit_list = my_fruit_list.set_index('Fruit')

# Pick list to pick fruit desired
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display the table in the frame
streamlit.dataframe(fruits_to_show)
# streamlit.text(fruityvice_response)

# create a code block (function) and define it
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

# New section to display fruityvice API response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?') # took out 'Kiwi' default
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

# stop here for the moment to troubleshoot
# creating a button above the streamlit.stop() line
streamlit.header("The fruit load list contains:")
# Snowflake related functions
def get_fruit_load_list():
    with    my_cnx.cursor() as my_cur:
            my_cur.execute("SELECT * FROM fruit_load_list")
            return my_cur.fetchall()
        
# add a button to load the fruit
if  streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"]) 
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

# allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
    with    my_cnx.cursor() as my_cur:
            my_cur.execute("INSERT INTO fruit_load_list VALUES ('" + new_fruit + "')")
            return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"]) 
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)
    
# streamlit.write('Thanks for adding ', add_my_fruit)


streamlit.stop()

