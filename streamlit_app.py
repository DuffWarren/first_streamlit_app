import streamlit
import pandas
import requests
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

#Fruit Picker
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

#streamlit.dataframe(my_fruit_list)


# Pick list to pick fruit desired
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display the table in the frame
streamlit.dataframe(fruits_to_show)
# streamlit.text(fruityvice_response)

streamlit.header("Fruityvice Fruit Advice!")
# New section to diplay fruityvice API response
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#streamlit.text(fruityvice_response.json())
# normalize the ugly text
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# Output screen as a table
streamlit.dataframe(fruityvice_normalized)

import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

fruit_choice_2 = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('The user entered ', fruit_choice_2)

Streamlit.write('Thanks for adding ', add_my_fruit)
# below will not work due to flow control issues
my_cur.execute("INSERT INTO fruit_load_list VALUES ('from streamlit')")
