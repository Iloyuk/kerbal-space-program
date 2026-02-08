import logging
import streamlit as st
import requests
import json
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')

SideBarLinks()

st.write("# Star System Database")

view, add, edit, delete = st.tabs(['View', 'Add', 'Edit', 'Delete'])

with view:
    with st.form("lookup"):
        st.write('**Lookup a star system in a galaxy, either by galaxy, star system, or a combination of both**')
        galaxy = st.text_input("Enter galaxy name/id *(leave this blank if searching by star system id)*:")
        star_sys = st.text_input("Enter star system name/id *(this can be blank if searching galaxies)*:")
        submitted = st.form_submit_button('Search')

        if submitted:
            if '/' in galaxy or '\\' in galaxy:
                st.error("Please enter a valid galaxy name/id for lookup")
            elif len(galaxy) == 0:
                if len(star_sys) > 0 and star_sys.isnumeric():
                    data = requests.get(f'http://api:4000/starsystems/{star_sys}').json()
                    if not data:
                        st.error("Could not find the star system")
                    else:
                        st.dataframe(data)
                else:
                    st.dataframe(requests.get('http://api:4000/galaxies/names').json())
            elif len(star_sys) == 0:  # If user only entered galaxy for search
                try:
                    data = requests.get(f'http://api:4000/galaxies/{galaxy}/starsystems').json()
                    if not data:
                        st.error("Could not find the galaxy, or galaxy contains no star systems")
                    else:
                        st.dataframe(data)
                except requests.exceptions.RequestException as e:
                    st.error("Could not retrieve data.")
                    st.text(f"Details: {e}")
            else:  # Search with both galaxy info and star system info
                if '/' in star_sys or '\\' in star_sys:
                    st.error("Please enter a valid star system name/id for lookup")
                else:
                    try:
                        if star_sys.isnumeric():
                            data = requests.get(f'http://api:4000/starsystems/{star_sys}').json()
                        else:
                            data = requests.get(f'http://api:4000/galaxies/{galaxy}/starsystems/{star_sys}').json()

                        if not data:
                            st.error("Could not find the star system")
                        else:
                            st.dataframe(data)
                    except requests.exceptions.RequestException as e:
                        st.error("Could not retrieve data.")
                        st.text(f"Details: {e}")
        else:
            st.dataframe(requests.get('http://api:4000/galaxies/names').json())

with add:
    with st.form("input"):
        st.write("**Add a new star system to the database**")
        system_name = st.text_input("*Star System Name:*")
        galaxy_id = st.text_input("Galaxy ID:")
        dist_in_ly = st.text_input("Dist. In Light Years:")
        system_type = st.text_input("Star System Type (Binary, Multiple):")
        num_stars = st.text_input("Num. of Stars:")
        submitted = st.form_submit_button('Add')

        if submitted:
            try:
                response = requests.post(f'http://api:4000/galaxies/{galaxy_id}/starsystems', json={
                    "SystemName": system_name if system_name != "" else None,
                    "DistInLY": dist_in_ly,
                    "SystemType": system_type,
                    "NumStars": num_stars
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
        st.write('**Modify an existing star system**')
        system_id = st.text_input("*Star System ID to be modified:*")
        system_name = st.text_input("Star System Name:")
        galaxy_id = st.text_input("Galaxy ID:")
        dist_in_ly = st.text_input("Dist. In Light Years:")
        system_type = st.text_input("Star System Type (Binary, Multiple):")
        num_stars = st.text_input("Num. of Stars:")
        submitted = st.form_submit_button('Modify')

        if submitted:
            try:
                response = requests.put(f'http://api:4000/galaxies/{galaxy_id}/starsystems', json={
                    "SystemName": system_name,
                    "SystemID": system_id,
                    "DistInLY": dist_in_ly,
                    "SystemType": system_type,
                    "NumStars": num_stars,
                })

                if response.status_code == 200:
                    result = response.json()
                    if result.get('rows_affected') == 0:
                        st.warning("No star system was updated")
                    else:
                        st.success("Star system updated successfully!")
                else:
                    error = response.json().get("error", "Unknown error occurred.")
                    st.error(f"Update failed: {error}")

            except requests.exceptions.RequestException as e:
                st.error("Could not update data.")
                st.text(f"Details: {e}")

with delete:
    with st.form("delete"):
        st.write("**Delete a star system**")
        star_sys_id = st.text_input("*Star System ID to be deleted:*")

        if st.form_submit_button("Delete"):
            try:
                response = requests.delete(f'http://api:4000/starsystems/{star_sys_id}',)
                if response.status_code == 200:
                    st.success("Star System deleted successfully!")
                else:
                    st.warning("No star system was deleted")
            except requests.exceptions.RequestException as e:
                st.error("Could not delete data.")
                st.text(f"Details: {e}")