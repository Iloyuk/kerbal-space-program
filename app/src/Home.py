##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

# streamlit supports regular and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout='wide')

# If a user is at this page, we assume they are not 
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel. 
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

# set the title of the page and provide a simple prompt. 
logger.info("Loading the Home page of the app")
st.title('NYASA\'s Kerbal Space Program')
st.write('\n\n')
st.write('### WELCOME! Which user would you like to log in as?')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user 
# can click to MIMIC logging in as that mock user.
if st.button('Act as Alex, a student who enjoys studying astronomy',
             type='primary',
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'student'
    st.session_state['first_name'] = 'Alex'
    st.switch_page('pages/100_Student_Home.py')

if st.button('Act as Carl, a mission control engineer',
             type='primary',
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'mission_control_engineer',
    st.session_state['first_name'] = 'Carl'
    st.switch_page('pages/110_MS_Engineer_Home.py')

if st.button('Act as Sammy, an astronomy research scientist',
             type='primary',
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'research_scientist',
    st.session_state['first_name'] = 'Sammy'
    st.switch_page('pages/120_Scientist_Home.py')

if st.button('Act as Lexie, a hobbyist astrologer',
             type='primary',
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'astrologer',
    st.session_state['first_name'] = 'Lexie'
    st.switch_page('pages/130_Astrologist_Home.py')
