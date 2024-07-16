import streamlit as st
from about import about_page
from products_services import products_services_page
from job_roles import job_roles_page
from team_builder import team_builder_page
from streamlit_navigation_bar import st_navbar

# Set the page configuration
st.set_page_config(page_title="Connext Global Solutions", page_icon="🌐", layout="wide")

page = st_navbar(["Home", "About Us", "Products and Services", "Job Role Requirements"])
# Page Navigation
if page == "Home":
    team_builder_page()
elif page == "About Us":
    about_page()
elif page == "Products and Services":
    products_services_page()
elif page == "Job Role Requirements":
    job_roles_page()
