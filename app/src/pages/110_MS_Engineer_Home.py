import logging
import requests
import streamlit as st
from modules.nav import SideBarLinks
logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')

SideBarLinks()

#Things to do:
# - /galaxies/{galaxyID}/starsystems
# - /missions
# - /missions/{missionID}
# - /spacecraft
# - /spacecraft/{spacecraftID}
# - /astronauts
# - /astronauts/{astronautID}
# - /spacecraft/{spacecraftID}/parts
# - /spacecraft/{spacecraftID}/parts/{partID}
# - /findings
# - /findings/{findingID}

st.title(f"Welcome, {st.session_state.first_name}")
st.write('### Here is a list of all missions')

with st.form("help"):
    title = st.text_input("Mission Name")
    if '/' in title or '\\' in title or not title:
        data = requests.get('http://api:4000/missions/objective').json()
    else:
        data = requests.get(f'http://api:4000/missions/name/{title}').json()
        if not data:
            data = requests.get('http://api:4000/missions/objective').json()

    st.form_submit_button('Update')
    st.dataframe(data)

if st.button('View all findings',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/111_Findings.py')

if st.button('View all spacecraft',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/112_All_Spacecraft.py')

if st.button('View missions in detail',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/113_Mission_Detail.py')