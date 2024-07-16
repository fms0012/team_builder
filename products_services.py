import streamlit as st
import requests
from streamlit_lottie import st_lottie

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Lottie animation
lottie_products_services = load_lottie_url('https://lottie.host/1b5fcd32-adcd-40f3-aef0-bb6ab0b7a657/oWek5O0BSz.json')  

def products_services_page():
    st.markdown("""
        <style>
        .center-content {
            display: flex;
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
       .Services {
            font-size:50px;
            text-align: center;
       }
       .Products{
            font-size:50px;
            text-align: center;
       }
        </style>
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                    }
                });
            });
            document.querySelectorAll('.animated-section').forEach(item => observer.observe(item));
        });
        </script>
    """, unsafe_allow_html=True)

    if lottie_products_services:
        st_lottie(lottie_products_services, height=300, key="products_services")

    st.markdown("<h1 class='title'>Products and Services</h1>", unsafe_allow_html=True)

    st.markdown("""
        <h2 class='Services'>Our Services</h2>
        <p class="center-text">Connext Global Solutions offers a wide range of services to support your business needs:</p>

        <h3 class="center-text">Recruiting</h3>
        <p class="center-text">Our recruiting services ensure that you get the best talent for your team. We handle the entire recruitment process from sourcing to onboarding.</p>

        <h3 class="center-text">Payroll</h3>
        <p class="center-text">We manage payroll processing, ensuring compliance with local and international regulations.</p>

        <h3 class="center-text">Compliance</h3>
        <p class="center-text">Our compliance services help you navigate the complexities of legal and regulatory requirements in different countries.</p>

        <h3 class="center-text">IT Support</h3>
        <p class="center-text">We provide comprehensive IT support services to ensure your technology infrastructure runs smoothly.</p>

        <h3 class="center-text">Facilities Management</h3>
        <p class="center-text">Our facilities management services cover everything from office setup to maintenance, ensuring a productive work environment.</p>

        <h3 class="center-text">Management Support</h3>
        <p class="center-text">We offer management support services to help you oversee and manage your offshore teams effectively.</p>
    """, unsafe_allow_html=True)

    st.markdown("""
       <h2 class='Products'>Our Products</h2>
        <p class="center-text">We offer a range of products designed to enhance productivity and efficiency:</p>

        <h3 class="center-text">Team Builder</h3>
        <p class="center-text">Our Team Builder tool helps you identify the right talent and build high-performing teams.</p>

        <h3 class="center-text">Payroll System</h3>
        <p class="center-text">Our robust payroll system ensures accurate and timely payment processing.</p>

        <h3 class="center-text">Compliance Tracker</h3>
        <p class="center-text">Our compliance tracker helps you stay on top of regulatory requirements and avoid legal issues.</p>
 
    """, unsafe_allow_html=True)

