import logging
import streamlit as st
from modules.nav import SideBarLinks
logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')

SideBarLinks()

st.title(f"Welcome, {st.session_state.first_name}")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Access the galaxy database',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/121_Galaxy_Data.py')

if st.button('Access the star system database',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/122_Star_System_Data.py')

if st.button('Access the star database',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/123_Star_Data.py')

if st.button('Access the planet database',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/124_Planet_Data.py')