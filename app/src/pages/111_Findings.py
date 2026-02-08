import logging
import numbers
logger = logging.getLogger(__name__)
import requests
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

SideBarLinks()

#Things to do:
# - /galaxies/{galaxyID}/starsystems
# - /missions  X
# - /missions/{missionID}  X
# - /spacecraft
# - /spacecraft/{spacecraftID}
# - /astronauts
# - /astronauts/{astronautID}
# - /spacecraft/{spacecraftID}/parts
# - /spacecraft/{spacecraftID}/parts/{partID}
# - /findings X
# - /findings/{findingID}  X

st.title("Findings for all missions")
#searching for specific mission
tab1,tab2 = st.tabs(['View', 'Add'])
with tab1:
    with st.form("wah"):
        data = requests.get('http://api:4000/findings').json()
        st.dataframe(data)
        title = st.number_input("Search by Name or ID",value=None,placeholder="Type a number...",step=1)
        searchFinding = st.checkbox("Search Finding ID")
        searchMission = st.checkbox("Search Mission ID")
        findingSearch = {}
        missionSearch = {}
        findingSelect = {}
        findingNotes = None
        findingSig = None   
        update = st.form_submit_button('Update')
        if update:
            if int(title): 
                if searchFinding:
                    findingSearch = requests.get(f'http://api:4000/findings/{title}').json()
                    findingNotes = st.text_input("Notes")
                    findingSig = st.text_input("Significance")
                if searchMission: 
                    missionSearch = requests.get(f'http://api:4000/missions/{title}/findings').json()
                    findingSelect = st.number_input("FindingID Select",step=1,value=None)
                if findingSearch:  st.dataframe(findingSearch)
                if searchMission: st.dataframe(missionSearch) 
            if findingNotes != None and findingNotes != "":
                response = requests.put(f'http://api:4000/findings/{title}/Notes/{findingNotes}')
                if response.status_code == 200:
                    st.success("Update successful!")
            if findingSig != None and findingSig != "":
                response = requests.put(f'http://api:4000/findings/{title}/Sig/{findingSig}')
                if response.status_code == 200:
                    st.success("Update successful!")
            for misfind in missionSearch:
                if misfind['FindingID'] != findingSelect:
                    for finding in data:
                        if finding['FindingID'] == findingSelect: 
                            response = requests.post(f'http://api:4000/missions/{title}/findings/{findingSelect}')
                            if response.status_code == 200:
                                st.success("Connection successful!")
                            break
                    break
with tab2:
    with st.form("input"):
        st.write('Add new findings')
        sig = st.selectbox('Significance', ('Low','Medium','High'))
        findDate = st.date_input('FindingDate')
        notes= st.text_input('Notes')
        submitted = st.form_submit_button('Add')

        if submitted:
            try:
                response = requests.post('http://api:4000/findings', json={
                    "Significance": sig,
                    "FindingDate": str(findDate),
                    "Notes": notes,
                })

                if response.status_code == 200:
                    st.success("Finding inserted successfully!")
                else:
                    st.error(response.json().get("error", "Unknown error"))
            except requests.exceptions.RequestException as e:
                st.error("Could not retrieve data.")
                st.text(f"Details: {e}")    
        


