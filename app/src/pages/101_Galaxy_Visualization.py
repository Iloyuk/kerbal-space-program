import logging
import requests
import streamlit as st
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

SideBarLinks()

st.header('Galaxy Visualization')

amount = int(st.number_input("Amount of galaxies you would like to display:", min_value=0, step=1, format="%d"))
data = requests.get('http://api:4000/galaxies', params={"amount": amount}).json()
st.dataframe(data)

with st.form("Galaxy Searcher"):
    GalaxyID = st.number_input("Search in Galaxy", value=None, step=1)
    viewStarSystem = st.checkbox("View Star System")
    viewStars = st.checkbox("View Stars")
    viewPlanets = st.checkbox("View Planets")
    update = st.form_submit_button('Update')
    if update:
        if GalaxyID:
            stars = []
            verif = False
            for a in data:
                if a['GalaxyID'] == GalaxyID:
                    verif = True
                    break
            if verif:
                systems = requests.get(f'http://api:4000/galaxies/{GalaxyID}/starsystems').json()
                if systems and viewStarSystem:
                    st.write("Star systems in galaxy:")
                    st.dataframe(systems)
                star = {}
                if viewStars:
                    st.write("Stars in galaxy:")
                for system in systems:
                    StarSysID = system['SystemID']
                    star = requests.get(f'http://api:4000/star_systems/{StarSysID}').json()
                    if star:
                        stars.append(star)
                        if viewStars:
                            st.dataframe(star)
                if viewPlanets:
                    st.write("Planets in galaxy:")
                    for s in stars:
                        for sta in s:
                            starID = sta['StarID']
                            planet = requests.get(
                                f'http://api:4000/planets/orbits',params={"star":starID}).json()
                            if planet:
                                st.dataframe(planet)