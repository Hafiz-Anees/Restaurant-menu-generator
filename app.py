import streamlit as st
import restaurant_name_menu_generator
st.title("Restaurant Name Generator")

cuisine = st.sidebar.selectbox("Pick a Cuisine",("Indian","Pakistani","Italian","Maxicon"))



if cuisine:
    response = restaurant_name_menu_generator.get_name_item(cuisine)
    st.header(response['restaurant_name'].strip())
    menu_items =  response['menu_items'].strip().split(",")
    st.write("***Menu item***")
    for item in menu_items:
        st.write("-",item)