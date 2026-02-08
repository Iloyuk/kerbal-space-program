import logging
logger = logging.getLogger(__name__)
import requests
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

SideBarLinks()
st.title("Astronaut Data")
tab1,tab2 = st.tabs(["View", "Edit"])
with tab1:
    with st.form("aaa"):
        data = requests.get('http://api:4000/astronauts').json()
        st.dataframe(data)
        selection = st.selectbox('Search',('Search by Name', 'Search by ID'))
        update = st.form_submit_button('Update')
        if selection == 'Search by Name':
            input = st.text_input("Search by Name")
        if selection == 'Search by ID':
            input = st.number_input("Search by ID",value=None, step=1)
        if update:
            if input:
                if selection == 'Search by Name':
                    response = requests.get(f'http://api:4000/astronauts/name/"{input}"')
                elif selection == 'Search by ID':
                    response = requests.get(f'http://api:4000/astronauts/{input}')
                response.raise_for_status()
                result = response.json()
                if result:
                    st.dataframe(result)
                    for i in result:
                        ID = i['AstroID']
                        mission = requests.get(f'http://api:4000/astronauts/{ID}/missions').json()
                        st.dataframe(mission)
with tab2:
    with st.form("aaaa"):
        data = requests.get('http://api:4000/astronauts').json()
        st.dataframe(data)
        selection = st.selectbox('Search',('Update', 'Add', 'Delete'))
        update = st.form_submit_button('Commit')
        refresh = st.form_submit_button('Refresh')
        ID = st.number_input("ID",value=None, step=1)
        Country = st.text_input("Country")
        YearsInSpace = st.number_input("Years in Space",value=None, step=1)
        Name = st.text_input("Name")
        if update:
            try:
                verif = False
                for a in data:
                    if a['AstroID'] == ID:
                        verif = True
                        break
                if ID and verif:
                    if selection == 'Update':
                        st.write("in update mode!")
                        if Country and Country != "":
                            request = requests.put(f'http://api:4000/astronauts/{ID}/country/{Country}')
                        if YearsInSpace:
                            request = requests.put(f'http://api:4000/astronauts/{ID}/yearsinspace/{YearsInSpace}')
                        if Name and Name != "":
                            request = requests.put(f'http://api:4000/astronauts/{ID}/name/{Name}')
                        if request.status_code == 200:
                            st.success("update successful!")
                        if request.status_code == 500:
                            st.error("There appears to be an error with the code. Let Davey know or something")
                    if selection == 'Delete':
                        st.write("in delete mode!")
                        request = requests.delete(f'http://api:4000/astronauts/{ID}')
                        if request.status_code == 200:
                            st.success("Delete successful!")
                        if request.status_code == 500:
                            st.error("There appears to be an error with the code. Let Davey know or something")
                if selection == 'Add':
                    st.write("in add mode!")
                    request = requests.post(f'http://api:4000/astronauts', json={
                        "Name": Name,
                        "Country": Country,
                        "YearsInSpace": YearsInSpace
                    })
                    if request.status_code == 200:
                        st.success("Addition successful!")
                    if request.status_code == 500:
                        st.error("There appears to be an error with the code. Let Davey know or something")
            except Exception as e:
                st.error("An error has occured")
                st.text(f"Details: {e}")
        if refresh:
            if selection == 'Update':
                st.write("in update mode!")
            if selection == 'Delete':
                st.write("in delete mode!")
            if selection == 'Add':
                st.write("in add mode!")


                
                


            