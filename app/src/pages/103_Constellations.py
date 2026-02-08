import logging
import requests
import streamlit as st
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

SideBarLinks()

st.header('Details on Planets')

data = requests.get('http://api:4000/constellation').json()
st.dataframe(data)
with st.form("constell"):
    ConstID = st.number_input("Search in Constellation ID", value=None, step=1)
    update = st.form_submit_button('Update')
    viewAllStars = st.checkbox("View Stars")
    if update:
        if ConstID:
            verif = False
            for a in data:
                if a['ConstID'] == ConstID:
                    verif = True
                    break
            if verif:
                data2 = requests.get(f'http://api:4000/constellation/{ConstID}').json()
                st.dataframe(data2)
                if viewAllStars:
                    data3 = requests.get(f'http://api:4000/constellation/{ConstID}/stars').json()
                    st.dataframe(data3)
