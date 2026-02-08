import logging
import streamlit as st
import requests
import json
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
from datetime import date

logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')

SideBarLinks()

st.write("# Galaxy Database")

view, add, edit, delete = st.tabs(['View', 'Add', 'Edit', 'Delete'])

with view:
    with st.form("lookup"):
        st.write('**Lookup galaxy**')
        galaxy = st.text_input("Enter galaxy name/id:")
        st.form_submit_button('Search')
        if '/' in galaxy or '\\' in galaxy or len(galaxy) == 0:
            data = requests.get('http://api:4000/galaxies', params={"amount": 10}).json()
        else:
            data = requests.get(f'http://api:4000/galaxies/{galaxy}').json()
            if not data:
                data = requests.get('http://api:4000/galaxies', params={"amount": 10}).json()
        st.dataframe(data)

with add:
    with st.form("input"):
        st.write('**Add a new galaxy to the database**')
        galaxy_name = st.text_input('Galaxy Name:')
        redshift = st.text_input('Redshift:')
        year_discovered = st.date_input("Date Discovered")
        solar_mass = st.text_input('Solar Mass in Trillions:')
        dominant_element = st.text_input('Dominant Element:')
        submitted = st.form_submit_button('Add')

        if submitted:
            try:
                response = requests.post('http://api:4000/galaxies', json={
                    "GalaxyName": galaxy_name if galaxy_name != "" else None,
                    "Redshift": redshift if redshift != "" else None,
                    "YearDiscovered": year_discovered.strftime('%Y-%m-%d') if isinstance(year_discovered, date) else year_discovered,
                    "SolarMassTrillions": solar_mass if solar_mass != "" else None,
                    "DominantElement": dominant_element if dominant_element != "" else None
                })

                if response.status_code == 200:
                    st.success("Galaxy inserted successfully!")
                else:
                    st.error(response.json().get("error", "Unknown error"))
            except requests.exceptions.RequestException as e:
                st.error("Could not insert data.")
                st.text(f"Details: {e}")

with edit:
    with st.form("replace"):
        st.write('**Modify an existing galaxy**')
        galaxy_id = st.text_input('*Galaxy ID to be modified:*')
        galaxy_name = st.text_input('Galaxy Name:')
        redshift = st.text_input('Redshift:')
        year_discovered = st.date_input("Date Discovered")
        solar_mass = st.text_input('Solar Mass in Trillions:')
        dominant_element = st.text_input('Dominant Element:')
        submitted = st.form_submit_button('Modify')

        if submitted:
            try:
                response = requests.put('http://api:4000/galaxies', json={
                    "GalaxyID": galaxy_id,
                    "GalaxyName": galaxy_name,
                    "Redshift": redshift,
                    "YearDiscovered": year_discovered.strftime('%Y-%m-%d') if isinstance(year_discovered, date) else year_discovered,
                    "SolarMassTrillions": solar_mass,
                    "DominantElement": dominant_element
                })

                if response.status_code == 200:
                    result = response.json()
                    if result.get('rows_affected') == 0:
                        st.warning("No galaxy was updated")
                    else:
                        st.success("Galaxy updated successfully!")
                else:
                    error = response.json().get("error", "Unknown error occurred.")
                    st.error(f"Update failed: {error}")

            except requests.exceptions.RequestException as e:
                st.error("Could not update data.")
                st.text(f"Details: {e}")

with delete:
    with st.form("delete"):
        st.write("**Delete a galaxy. WARNING: THIS WILL DELETE ALL STAR SYSTEMS IN SAID GALAXY**")
        galaxy_id = st.text_input("*Galaxy ID to be deleted:*")

        if st.form_submit_button("Delete"):
            try:
                response = requests.delete(f'http://api:4000/galaxies', params={"GalaxyID": galaxy_id})
                if response.status_code == 200:
                    st.success("Galaxy deleted successfully!")
                else:
                    st.warning("No galaxy was deleted")
            except requests.exceptions.RequestException as e:
                st.error("Could not delete data.")
                st.text(f"Details: {e}")
