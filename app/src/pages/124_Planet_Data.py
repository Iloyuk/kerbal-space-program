import logging
import streamlit as st
import requests
import json
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')

SideBarLinks()

st.write("# Planet Database")

view, planets, orbits = st.tabs(['View Planets/Orbits', 'Modify Planets', 'Modify Orbits'])

with view:
    with st.form("lookup_star"):
        st.write('**Search a star\'s orbits**')
        star = st.text_input("Enter star name/id:")

        if st.form_submit_button('Search'):
            if '/' in star or '\\' in star or len(star) == 0:
                st.error("Please enter a valid star name/id")
            else:
                data = requests.get(f'http://api:4000/planets/orbits',
                                    params={"star": star}).json()
                if not data:
                    st.error("Could not find star")
                else:
                    st.dataframe(data)

    with st.form("lookup_planet"):
        st.write('**Lookup information on a planet**')
        planet_identifier = st.text_input("Enter planet name/id:")

        if st.form_submit_button('Search'):
            if '/' in planet_identifier or '\\' in planet_identifier or len(planet_identifier) == 0:
                st.error("Please enter a valid planet name/id")
            else:
                data = requests.get(f'http://api:4000/planets/{planet_identifier}').json()
                if not data:
                    st.error("Could not find planet")
                else:
                    st.dataframe(data)

with planets:
    with st.form("input_planet"):
        st.write('**Add a new planet to the database**')
        planet_name = st.text_input("Planet Name:")
        planet_type = st.text_input("Planet Type:")
        mass = st.text_input("Mass:")
        num_moons = st.text_input("Num. of Moons:")
        eccentricity = st.text_input("Eccentricity:")
        inclination = st.text_input("Inclination:")

        if st.form_submit_button("Add"):
            try:
                response = requests.post('http://api:4000/planets', json={
                    "PlanetName": planet_name if planet_name != "" else None,
                    "PlanetType": planet_type,
                    "Mass": mass if mass != "" else None,
                    "NumMoons": num_moons if num_moons != "" else None,
                    "Eccentricity": eccentricity if eccentricity != "" else None,
                    "Inclination": inclination if inclination != "" else None
                })
                if response.status_code == 200:
                    st.success("Planet added successfully!")
                else:
                    st.error(response.json().get("error", "Unknown error"))
            except Exception as e:
                st.error("Could not insert data.")
                st.text(f"Details: {e}")

    with st.form("update_planet"):
        st.write('**Update a planet**')
        planet_id = st.text_input("*Planet ID to be modified:*")
        planet_name = st.text_input("Planet Name:")
        planet_type = st.text_input("Planet Type:")
        mass = st.text_input("Mass:")
        num_moons = st.text_input("Num. of Moons:")
        eccentricity = st.text_input("Eccentricity:")
        inclination = st.text_input("Inclination:")

        if st.form_submit_button("Update"):
            try:
                response = requests.put('http://api:4000/planets', json={
                    "PlanetName": planet_name,
                    "PlanetType": planet_type,
                    "Mass": mass,
                    "NumMoons": num_moons,
                    "Eccentricity": eccentricity,
                    "Inclination": inclination,
                    "PlanetID": planet_id
                })

                if response.status_code == 200:
                    result = response.json()
                    if result.get('rows_affected') == 0:
                        st.warning("No planet was updated")
                    else:
                        st.success("Planet updated successfully!")
                else:
                    error = response.json().get("error", "Unknown error occurred.")
                    st.error(f"Update failed: {error}")

            except requests.exceptions.RequestException as e:
                st.error("Could not update data.")
                st.text(f"Details: {e}")

    with st.form("delete_planet"):
        st.write('**Delete a planet**')
        planet_id = st.text_input("*Planet ID to be deleted:*")

        if st.form_submit_button("Delete"):
            try:
                response = requests.delete(f'http://api:4000/planets', params={"PlanetID": planet_id})
                if response.status_code == 200:
                    st.success("Planet deleted successfully!")
                else:
                    st.warning("No planet was deleted")
            except requests.exceptions.RequestException as e:
                st.error("Could not delete data.")
                st.text(f"Details: {e}")

with orbits:
    with st.form("input_orbit"):
        st.write('**Add a new planet\'s orbital status to the database**')
        planet_id = st.text_input("*Planet ID:*")
        star_id = st.text_input("*Star ID:*")
        orbital_period = st.text_input("Orbital Period:")
        semi_major_axis = st.text_input("Semi-major axis:")

        if st.form_submit_button("Add"):
            try:
                response = requests.post('http://api:4000/planets/orbits', json={
                    "PlanetID": planet_id,
                    "StarID": star_id,
                    "OrbitalPeriod": orbital_period if orbital_period != "" else None,
                    "SemiMajorAxis": semi_major_axis if semi_major_axis != "" else None
                })

                if response.status_code == 200:
                    st.success("Planet added successfully!")
                else:
                    error = response.json().get("error", "Unknown error occurred.")
            except requests.exceptions.RequestException as e:
                st.error("Could not insert data.")
                st.text(f"Details: {e}")

    with st.form("update_orbit"):
        st.write('**Update a planet\'s orbital status**')
        planet_id = st.text_input("*Planet ID to be modified:*")
        star_id = st.text_input("Star ID:")
        orbital_period = st.text_input("Orbital Period:")
        semi_major_axis = st.text_input("Semi-major axis:")

        if st.form_submit_button("Update"):
            try:
                response = requests.put('http://api:4000/planets/orbits', json={
                    "PlanetID": planet_id,
                    "StarID": star_id,
                    "OrbitalPeriod": orbital_period if orbital_period != "" else None,
                    "SemiMajorAxis": semi_major_axis if semi_major_axis != "" else None
                })

                if response.status_code == 200:
                    result = response.json()
                    if result.get('rows_affected') == 0:
                        st.warning("No orbital status was updated")
                    else:
                        st.success("Orbital status updated successfully!")
                else:
                    error = response.json().get("error", "Unknown error occurred.")
                    st.error(f"Update failed: {error}")

            except requests.exceptions.RequestException as e:
                st.error("Could not update data.")
                st.text(f"Details: {e}")

    with st.form("delete_orbit"):
        st.write('**Delete a planet\'s orbital info**')
        star_id = st.text_input("*Orbit's Star ID:*")
        planet_id = st.text_input("*Orbit's Planet ID:*")

        if st.form_submit_button("Delete"):
            try:
                response = requests.delete(f'http://api:4000/planets/orbits', json={
                    "PlanetID": planet_id,
                    "StarID": star_id
                })
                if response.status_code == 200:
                    st.success("Orbital information deleted successfully!")
                else:
                    st.warning("No information was deleted")
            except requests.exceptions.RequestException as e:
                st.error("Could not delete data.")
                st.text(f"Details: {e}")