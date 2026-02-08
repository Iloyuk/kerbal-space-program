import logging
import streamlit as st
import requests
import json
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')

SideBarLinks()

st.write("# Star Database")

view, add, edit, delete = st.tabs(['View', 'Add', 'Edit', 'Delete'])

with view:
    with st.form("lookup_star_system"):
        st.write('**Search a star system\'s stars**')
        star_sys = st.text_input("Enter star system name/id:")
        submitted = st.form_submit_button('Search')

        if submitted:
            if '/' in star_sys or '\\' in star_sys or len(star_sys) == 0:
                st.error("Please enter a valid star system name/id")
            else:
                data = requests.get(f'http://api:4000/star_systems/{star_sys}').json()
                if not data:
                    st.error("Could not find star system")
                else:
                    st.dataframe(data)

    with st.form("lookup_star"):
        st.write('**Look up information on a star**')
        star = st.text_input("Enter star id:")
        submitted_star = st.form_submit_button('Search star information')
        submitted_planet = st.form_submit_button('Search planets which orbit this star')

        if submitted_star:
            if not star.isnumeric():
                st.error("Please enter a valid star id")
            else:
                data = requests.get(f'http://api:4000/stars/{star}').json()
                if not data:
                    st.error("Could not find star")
                else:
                    st.dataframe(data)

        if submitted_planet:
            if not star.isnumeric():
                st.error("Please enter a valid star id")
            else:
                data = requests.get(f'http://api:4000/planets/orbits',
                                    params={"star": star}).json()
                if not data:
                    st.error("Could not find star")
                else:
                    st.dataframe(data)

with add:
    with st.form("input"):
        st.write('**Add a new star to the database**')
        star_name = st.text_input("Star Name:")
        sys_id = st.text_input("Star System ID:")
        const_id = st.text_input("Constellation ID:")
        mass = st.text_input("Mass:")
        temp = st.text_input("Temperature:")
        spectral_type = st.text_input("Spectral Type:")
        submitted = st.form_submit_button('Add')

        if submitted:
            try:
                response = requests.post('http://api:4000/stars', json={
                    "SystemID": sys_id,
                    "ConstID": const_id if const_id != "" else None,
                    "StarName": star_name if star_name != "" else None,
                    "Mass": mass if mass != "" else None,
                    "Temperature": temp if temp != "" else None,
                    "SpectralType": spectral_type
                })

                if response.status_code == 200:
                    st.success("Star added successfully!")
                else:
                    st.error(response.json().get("error", "Unknown error"))
            except Exception as e:
                st.error("Could not insert data.")
                st.text(f"Details: {e}")

with edit:
    with st.form("update"):
        st.write('**Update a star**')
        star_id = st.text_input("*Star ID to be modified:*")
        star_name = st.text_input("Star Name:")
        sys_id = st.text_input("Star System ID:")
        const_id = st.text_input("Constellation ID:")
        mass = st.text_input("Mass:")
        temp = st.text_input("Temperature:")
        spectral_type = st.text_input("Spectral Type:")
        submitted = st.form_submit_button('Update')

        if submitted:
            try:
                response = requests.put('http://api:4000/stars', json={
                    "SystemID": sys_id,
                    "ConstID": const_id,
                    "StarName": star_name,
                    "Mass": mass,
                    "Temperature": temp,
                    "SpectralType": spectral_type,
                    "StarID": star_id
                })

                if response.status_code == 200:
                    result = response.json()
                    if result.get('rows_affected') == 0:
                        st.warning("No star was updated")
                    else:
                        st.success("Star updated successfully!")
                else:
                    error = response.json().get("error", "Unknown error occurred.")
                    st.error(f"Update failed: {error}")

            except requests.exceptions.RequestException as e:
                st.error("Could not update data.")
                st.text(f"Details: {e}")

with delete:
    with st.form("delete"):
        st.write("**Delete a star**")
        star_id = st.text_input("*Star ID to be deleted:*")

        if st.form_submit_button("Delete"):
            try:
                response = requests.delete(f'http://api:4000/stars', params={"StarID": star_id})
                if response.status_code == 200:
                    st.success("Star deleted successfully!")
                else:
                    st.warning("No star was deleted")
            except requests.exceptions.RequestException as e:
                st.error("Could not delete data.")
                st.text(f"Details: {e}")