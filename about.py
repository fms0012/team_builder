import streamlit as st
import requests
from streamlit_lottie import st_lottie

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Lottie animations
lottie_about_us = load_lottie_url('https://lottie.host/a4891845-4fe8-452b-a5fc-457334fb5f36/a9HN0Bjxy2.json')

def about_page():
    st.markdown("""
        <style>
        .center-content {
            text-align: center;
        }
        .center-image {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 50%;
        }
         .title {
            text-align: center;
            margin-top: 0;
            font-size:60px;
        }
        </style>
    """, unsafe_allow_html=True)

    if lottie_about_us:
        st_lottie(lottie_about_us, height=300, key="about_us")

    st.markdown("<h2 class='title'>About Us</h2>", unsafe_allow_html=True)

    st.markdown("""
    ### Connext Global Solutions
    Connext Global Solutions specializes in providing full-service offshore staffing and custom-built team solutions.
    We offer recruiting, payroll, compliance, IT, facilities, and management support to help businesses build high-performing global teams.

    """, unsafe_allow_html=True)

    st.markdown("""
    ### What We Do
    At Connext Global Solutions, we understand the unique challenges businesses face in today's competitive environment. 
    Our goal is to provide tailored offshore staffing solutions that meet the specific needs of each client, ensuring they have the resources necessary to succeed.

    ### Our Mission
    To deliver exceptional offshore staffing solutions that drive success for our clients.

    ### Our Vision
    To be the leading provider of customized offshore staffing solutions worldwide.

    ### Our Values
    - **Integrity:** We uphold the highest standards of integrity in all of our actions.
    - **Customer Commitment:** We develop relationships that make a positive difference in our customers' lives.
    - **Quality:** We provide outstanding products and unsurpassed service that, together, deliver premium value to our customers.
    - **Teamwork:** We work together, across boundaries, to meet the needs of our customers and to help the company win.

    ### Our Services
    - **Recruiting:** Identifying and attracting top talent to meet your staffing needs.
    - **Payroll:** Managing payroll processes efficiently and accurately.
    - **Compliance:** Ensuring adherence to all relevant regulations and standards.
    - **IT Support:** Providing reliable IT services to support your operations.
    - **Facilities Management:** Maintaining optimal working environments for your teams.
    - **Management Support:** Offering comprehensive management solutions to enhance productivity and performance.

    ### Leadership Team
    Our leadership team comprises experienced professionals dedicated to ensuring the highest quality of service and support. 
    They bring a wealth of knowledge and expertise to our organization, driving our mission and values forward.

    ### Why Choose Us?
    - **Customized Solutions:** We tailor our services to meet the unique needs of each client.
    - **Experienced Team:** Our team has the expertise to provide top-notch offshore staffing solutions.
    - **Proven Track Record:** We have a history of success in helping businesses achieve their goals.
    - **Global Reach:** Our services are designed to support businesses worldwide.

    ### Contact Us
    For more information about our services or to discuss your staffing needs, please contact us at [https://connextglobal.com](https://connextglobal.com).

    """, unsafe_allow_html=True)

