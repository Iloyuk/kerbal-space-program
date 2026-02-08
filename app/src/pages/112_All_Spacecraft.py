import logging
logger = logging.getLogger(__name__)
import requests
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title("Spacecraft")
with st.form("aaa"):
    data = requests.get('http://api:4000/spacecraft').json()
    st.dataframe(data)
    spacecraftID = st.number_input('Insert SpacecraftID', value=None, step=1)
    add= st.checkbox("Add Part")
    update = st.form_submit_button('Update')
    if update:
        if spacecraftID:
            for a in data:
                if a['ShipID'] == spacecraftID:
                    verif = True
                    break
            astronautData = requests.get(f'http://api:4000/astronauts/onShip/{spacecraftID}').json()
            partData = requests.get(f'http://api:4000/spacecraft/{spacecraftID}/parts').json()
            if astronautData:
                st.dataframe(astronautData)
            if partData:
                st.dataframe(partData)
    if add:
        addPart = st.form_submit_button('Add Part')
        name = st.text_input("Part Name")
        MassInTons = st.number_input("Mass In Tons", step=1, value=1)
        LengthInCM = st.number_input("Length in CM", step=1, value=1)
        partUsage = st.text_input("Part Usage")
        if addPart:
            try:
                if name and MassInTons and LengthInCM and partUsage:
                    query = requests.post(f'http://api:4000/spacecraft/{spacecraftID}/parts', json={
                        "PartName": name,
                        "MassInTons": MassInTons,
                        "LengthInCM":LengthInCM,
                        "PartUsage":partUsage
                    })
                    if query.status_code == 200:
                        st.success("Part added successfully!")
                    if query.status_code == 500:
                        st.error("SQL Error")
            except Exception as e:
                st.error(f"Error: {e}")
if st.button('Astronaut Data/Info',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/114_Astronaut_Data.py')