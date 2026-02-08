import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title(f"Welcome, {st.session_state.first_name}")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View a galaxy chart',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/101_Galaxy_Visualization.py')

if st.button('Star Systems in detail',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/102_Star_System_Vis.py')

if st.button('Constellations',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/103_Constellations.py')
