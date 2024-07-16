import streamlit as st
import requests
from streamlit_lottie import st_lottie

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Lottie animation for job roles
lottie_job_roles = load_lottie_url('https://lottie.host/234f85b7-b1ac-48d1-992b-43b460c09b49/nISay8eX1k.json')  # Replace with an appropriate URL

def job_roles_page():
    st.markdown("""
        <style>
        .center-content {
            display: flexbox;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
        .center-text {
            text-align: center;
        }
       .title {
            text-align: center;
            margin-top: 0;
            font-size:60px;
        }
        </style>
    """, unsafe_allow_html=True)

    if lottie_job_roles:
        st_lottie(lottie_job_roles, height=300, key="job_roles")

    st.markdown("<h1 class='title'>Job Role Requirements</h1>", unsafe_allow_html=True)
    st.markdown("""
    ## Job Role Requirements

    ### Web Developer
    - **Responsibilities:**
      - Develop and maintain web applications
      - Ensure the technical feasibility of UI/UX designs
      - Optimize applications for maximum speed and scalability
    - **Requirements:**
      - Proven experience in web development
      - Familiarity with front-end technologies (e.g., HTML, CSS, JavaScript)
      - Experience with back-end languages (e.g., Python, PHP, Ruby)

    ### Accountant
    - **Responsibilities:**
      - Prepare and examine financial records
      - Ensure compliance with financial regulations
      - Analyze financial data and provide insights
    - **Requirements:**
      - Bachelor’s degree in Accounting or related field
      - Proven experience as an accountant
      - Strong knowledge of accounting principles and regulations

    ### 3D Graphic Artist
    - **Responsibilities:**
      - Create 3D models and animations
      - Collaborate with design teams to develop visual content
      - Optimize 3D assets for various platforms
    - **Requirements:**
      - Proven experience as a 3D artist
      - Proficiency with 3D software (e.g., Maya, Blender)
      - Strong portfolio showcasing 3D work
    """)

