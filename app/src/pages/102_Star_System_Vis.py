import logging
import requests
import streamlit as st
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

SideBarLinks()

st.header('Star System Visualization')
amount = int(st.number_input("Amount of galaxies you would like to display:", min_value=0, step=1, format="%d"))
galaxys = requests.get('http://api:4000/galaxies', params={"amount": amount}).json() #wrong name on purpose for funny
st.dataframe(galaxys)

with st.form("viewing the stars"):
    st.write('## Star System Viewer')
    GalaxyID = st.number_input("Search in Galaxy", value=None, step=1)
    box = st.selectbox("Select options",["View Graph", "View Stars"])
    update = st.form_submit_button('Update')
    if update:
        verif = False
        for a in galaxys:
            if a['GalaxyID'] == GalaxyID:
                verif = True
                break
        if verif and GalaxyID:
                systems = requests.get(f'http://api:4000/galaxies/{GalaxyID}/starsystems').json()
                if systems:
                    st.dataframe(systems)
                    if box == "View Graph":
                        newData = requests.get(f'http://api:4000/galaxies/{GalaxyID}/starsystems/distInLY').json()
                        st.bar_chart(newData, x='SystemID', y='DistInLY')
                    if box == "View Stars":
                        for system in systems:
                            StarSysID = system['SystemID']
                            star = requests.get(f'http://api:4000/star_systems/{StarSysID}').json()
                            st.dataframe(star)
            
