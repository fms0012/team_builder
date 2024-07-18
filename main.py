import streamlit as st
from about import about_page
from products_services import products_services_page
from job_roles import job_roles_page
from team_builder import team_builder_page
from streamlit_option_menu import option_menu

# Set the page configuration
st.set_page_config(page_title="Connext Global Solutions", page_icon="🌐", layout="wide")

# Create a sidebar with a navigation menu
with st.sidebar:
    page = option_menu(
        "Main Menu", ["Home", "About Us", "Products and Services", "Job Role Requirements"],
        icons=["house", "info-circle", "briefcase", "list-task"],
        menu_icon="cast", default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#f0f0f0"},
            "icon": {"color": "blue", "font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "green"},
        }
    )

# Page Navigation
if page == "Home":
    team_builder_page()
elif page == "About Us":
    about_page()
elif page == "Products and Services":
    products_services_page()
elif page == "Job Role Requirements":
    job_roles_page()

