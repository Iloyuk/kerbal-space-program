import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

with st.container():
    st.markdown (
        """
        The Kerbal Space Program database app was made by Jason, Davey, and Kylie. 

        It is a database app that keep tracks of galaxies, stars, star systems, and more, with the ability to update
        it and view, made with the intent of easy control and identifiable info. 
        """
            )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("assets/faust.png", width=270, caption="hello! - davey")

    with col2:
        st.image("assets/skye.png", width=256, caption="sammy killed my will to live - jason")

    with col3:
        st.image("assets/nug.png", width=272, caption="Every day when I go to work"
                                                      "\nI think about picking up my fork"
                                                      "\nAnd pushing it into some freshly baked"
                                                      "\nchicken nuggies that I have made"
                                                      "\n\nI love the shapes, the color, the size"
                                                      "\nEach one the same, but still a surprise"
                                                      "\nI love the taste of nuggies in my mouth"
                                                      "\nThat’s what life is all about"
                                                      "\n\nMy mom told me that we are what we eat"
                                                      "\nBut that can’t be true, or else I would be meat"
                                                      "\nMeat in a dinosaur shape, that is"
                                                      "\nI’m no good at math but I’m a dino nuggie whiz"
                                                      "\n\n\nNuggies, nuggies, hear my cry"
                                                      "\nToday is the day that you will die"
                                                      "\nI have made it my final mission"
                                                      "\nYou won't be spared under any condition"
                                                      "\n\nSometimes I've wondered where my nuggies are"
                                                      "\nI've looked in my room and in my car"
                                                      "\nBut my nuggies, they are nowhere to be seen"
                                                      "\nI begin to wonder if this is some sick dream"
                                                      "\n\nYou will not escape me today"
                                                      "\nYou nuggies should have known you would pay"
                                                      "\nEither in ranch or in barbecue sauce"
                                                      "\nAnd in a baking sheet you shall toss"
                                                      "\n\n\nI’ll take you out just as you crisp up"
                                                      "\nAnd I’ll eat you off the tray so there’s no cleanup"
                                                      "\nI’ll put you in my mouth and I’ll chew for a while"
                                                      "\nEating dino nuggies will always be in style"
                                                      "\n\nAfter I’m done with my nuggie surprise"
                                                      "\nI’ll put the box back into the freezer lengthwise"
                                                      "\nAnd even though the box must go away"
                                                      "\nThe nuggies will be here to stay"
                                                      "\n\nEating nuggies is never a chore"
                                                      "\nThe nuggie urge is something I cannot ignore"
                                                      "\nThe next time my tummy just wants to eat"
                                                      "\nI have just the thing; a Dino Nuggie treat. - kylie")
