import logging
import requests
import streamlit as st
from modules.nav import SideBarLinks
logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')

SideBarLinks()

data = {}
try:
    data = requests.get('http://api:4000/constellation').json()

    st.title("🌟 Information on all the constellations!")
    for constellation in data:
        st.write(f"### {constellation['ConstName']}")
        st.markdown(f"Also abbreviated as **{constellation['Abbreviation']}**. Located in the "
                    f"{constellation['Hemisphere']}ern hemisphere, and its brightest star "
                    f"is **{constellation['BrightestStar']}**. A fun fact: {constellation['Notes']}.")
except requests.exceptions.RequestException as e:
    st.write("Could not connect to API :c")
