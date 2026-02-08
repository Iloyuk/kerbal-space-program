# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st
import base64


#what i use to change the background - davey
@st.cache_data
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


# Alex
def AlexHome():
    st.sidebar.page_link("pages/100_Student_Home.py", label="Home", icon="🏠")


def GalaxyVis():
    st.sidebar.page_link("pages/101_Galaxy_Visualization.py", label="Galaxy Visualization", icon="🌌")


def StarVis():
    st.sidebar.page_link("pages/102_Star_System_Vis.py", label="Star System Visualization", icon="✨")


def Constellations():
    st.sidebar.page_link("pages/103_Constellations.py", label="Constellations", icon="⛎")


# Sammy
def SammyHome():
    st.sidebar.page_link("pages/120_Scientist_Home.py", label="Home", icon="🏠")


def Galaxy():
    st.sidebar.page_link("pages/121_Galaxy_Data.py", label="Galaxy Data", icon="🌌")


def StarSystem():
    st.sidebar.page_link("pages/122_Star_System_Data.py", label="Star System Data", icon="☄")


def Star():
    st.sidebar.page_link("pages/123_Star_Data.py", label="Star Data", icon="⭐")


def Planet():
    st.sidebar.page_link("pages/124_Planet_Data.py", label="Planet Data", icon="🪐")


# Lexie
def LexieHome():
    st.sidebar.page_link("pages/130_Astrologist_Home.py", label="Home", icon="🏠")


def ConstellationInfo():
    st.sidebar.page_link("pages/131_Constellation_Info.py", label="Constellation Information", icon="⛎")


def FindConstellation():
    st.sidebar.page_link("pages/132_Find_Constellation.py", label="Find constellation from star", icon="✨")


# Carl
def Findings():
    st.sidebar.page_link("pages/111_Findings.py", label="Findings", icon="🌟")


def CarlHomePage():
    st.sidebar.page_link("pages/110_MS_Engineer_Home.py", label="Missions/Home", icon="🖥️")


def Spacecraft():
    st.sidebar.page_link("pages/112_All_Spacecraft.py", label="Spacecraft", icon="🚀")


def Missions():
    st.sidebar.page_link("pages/113_Mission_Detail.py", label="Missions in Detail", icon="🔥")


def BackgroundImgSet():
    set_background("assets/galaxybackground.png")


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always    
    st.sidebar.image("assets/logo.png", width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:
        # alex
        if st.session_state.first_name == "Alex":
            AlexHome()
            GalaxyVis()
            StarVis()
            Constellations()
        # carl my goat
        if st.session_state.first_name == "Carl":
            CarlHomePage()
            Findings()
            Spacecraft()
            Missions()
        # sammy my woat >:(
        if st.session_state.first_name == "Sammy":
            SammyHome()
            Galaxy()
            StarSystem()
            Star()
            Planet()
        # lexie
        if st.session_state.first_name == "Lexie":
            LexieHome()
            ConstellationInfo()
            FindConstellation()


    # Always show the About page at the bottom of the list of links
    AboutPageNav()
    BackgroundImgSet()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
