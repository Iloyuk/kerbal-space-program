import logging
import requests
import streamlit as st
from modules.nav import SideBarLinks
logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')

SideBarLinks()

with st.form("star_lookup_form"):
    star = st.text_input("Enter the star name you wish to look up:")
    submitted = st.form_submit_button("Lookup Star")

if submitted:
    try:
        response = requests.get(f"http://api:4000/constellation/star/{star}")
        response.raise_for_status()
        data = response.json()

        if data:
            st.markdown(f"🌟 The star **{star}** is in the **{data[0]['ConstName']}** constellation.")
        else:
            st.warning(f"No constellation found for **{star}**.")
    except requests.exceptions.RequestException as e:
        st.error("Could not retrieve data.")
        st.text(f"Details: {e}")
