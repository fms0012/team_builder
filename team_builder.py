import streamlit as st
import pandas as pd
import json
import requests

# Function to interact with Llama3 API
def llama3_query(prompt):
    url = "http://localhost:8000/query"  # Adjust the URL as necessary for your local setup
    payload = {
        "prompt": prompt,
    }
    headers = {
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json().get('response')
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to Llama3 API: {e}")
        return None

# Function to extract job roles from the response
def extract_job_roles(response):
    prompt = f"Extract job roles from the following response: {response}"
    job_roles_response = llama3_query(prompt)
    if job_roles_response:
        job_roles = [job.strip() for job in job_roles_response.split(',')]  # Assuming comma-separated job roles
        return job_roles
    return []

# Function to get median salaries for job roles
def get_median_salaries(job_roles):
    job_roles_str = ", ".join(job_roles)
    salaries_prompt = f"Provide the median salaries in USD for each of the following job roles in the Philippines and the US: {job_roles_str}"
    salaries_response = llama3_query(salaries_prompt)
    if salaries_response:
        return json.loads(salaries_response)
    return {}

# Main Streamlit application
def main():
    st.title("Accurate Team Builder Application")

    response = st.text_area("Paste the response here", height=150)

    if st.button("Extract Job Roles"):
        job_roles = extract_job_roles(response)
        if job_roles:
            st.write(f"Extracted Job Roles: {job_roles}")
            st.session_state.job_roles = job_roles
        else:
            st.error("No job roles extracted. Please check the response and try again.")

    if 'job_roles' in st.session_state:
        job_roles = st.session_state.job_roles
        salaries_data = get_median_salaries(job_roles)
        
        if salaries_data:
            # Display salaries data
            df = pd.DataFrame.from_dict(salaries_data, orient='index')
            st.write(df)

            # Add number inputs for each job role
            num_inputs = {}
            for job_role in job_roles:
                num_inputs[job_role] = st.number_input(f"How many {job_role} would you like to acquire?", min_value=0, step=1)
            
            if st.button("Calculate Savings"):
                total_ph_salaries = sum([num_inputs[job_role] * df.loc[job_role, "Philippine Salary"] for job_role in job_roles])
                total_us_salaries = sum([num_inputs[job_role] * df.loc[job_role, "US Salary"] for job_role in job_roles])
                savings = total_us_salaries - total_ph_salaries
                
                st.write(f"Total Philippine Salaries: ${total_ph_salaries:.2f}")
                st.write(f"Total US Salaries: ${total_us_salaries:.2f}")
                st.write(f"Estimated Savings: ${savings:.2f}")

            # CSV download button
            csv = df.to_csv(index=True)
            st.download_button(label="Download as CSV", data=csv, file_name="salaries.csv", mime="text/csv")

            # Detailed job descriptions and skill requirements
            for job_role in job_roles:
                st.subheader(f"Details for {job_role}")
                job_detail_prompt = f"Provide a detailed job description and required skills for {job_role}"
                job_detail_response = llama3_query(job_detail_prompt)
                if job_detail_response:
                    st.write(job_detail_response)
                else:
                    st.error(f"Could not fetch details for {job_role}.")
        else:
            st.error("Failed to fetch median salaries. Please check the job roles and try again.")

if __name__ == "__main__":
    main()
