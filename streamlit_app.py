# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import pandas

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie!:cup_with_straw:")
st.write("Choose the fruits you want in your customize smoothie")

name_on_order = st.text_input("Name of smoothie:")
st.write("The name on your smoothie will be", name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()


pd_pf= my_dataframe.to_pandas()
#st.dataframe(pd_pf)
#st.stop()

ingredient_list = st.multiselect(
    'Choose upto 5 ingredients:',
    my_dataframe, max_selections=5
)
if ingredient_list:
 
    ingredients_string = ''
    
    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen + ' '
        search_on = pd_pf.loc[pd_pf['FRUIT_NAME']==fruit_chosen,'search_on'].iloc[0]
        st.subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data= smoothiefroot_response.json(), use_container_width = True)

    #st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    time_to_insert = st.button('Submit Order')

    st.write(my_insert_stmt)
    st.stop()
    

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
