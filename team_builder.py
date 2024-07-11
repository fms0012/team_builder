import streamlit as st
import pandas as pd
import openai
import ast
import json
import re
import io

# Set your OpenAI API key
openai.api_key = 'AIzaSyBYLXhvqwNsxNzMAMcxBlnAulcFOhNQhEk'

### Functions: START
def extract_and_convert_list(text):
    # Find a potential list in the string using regex
    list_match = re.search(r'\[.*?\]', text, re.DOTALL)
    
    if list_match:
        list_string = list_match.group()
        try:
            # Try to safely evaluate the string as a Python expression
            python_list = ast.literal_eval(list_string)
            if isinstance(python_list, list):
                return python_list
            else:
                return None  # The extracted content is not a list
        except (SyntaxError, ValueError):
            return None  # The extracted content is not a valid Python expression
    else:
        return None  # No list found in the string

def extract_and_parse_json(text):
    # Find the first opening and the last closing curly brackets
    start_index = text.find('{')
    end_index = text.rfind('}')
    
    if start_index == -1 or end_index == -1 or end_index < start_index:
        return None, False  # Proper JSON structure not found

    # Extract the substring that contains the JSON
    json_str = text[start_index:end_index + 1]

    try:
        # Attempt to parse the JSON
        parsed_json = json.loads(json_str)
        return parsed_json, True
    except json.JSONDecodeError:
        return None, False  # JSON parsing failed

def validate_and_convert_salary_json(json_input):
    # Check if the input is a dictionary and validate the required keys
    def is_valid_salary_comparison(data):
        # Check for the presence of all required keys
        return (
            "salary_comparison" in data and
            "philippines" in data["salary_comparison"] and
            "united_states" in data["salary_comparison"]
        )

    # If the input is already a dictionary, validate it directly
    if isinstance(json_input, dict):
        valid = is_valid_salary_comparison(json_input)
        return json_input, valid
    
    # If it's a string, attempt to parse it as JSON
    try:
        data = json.loads(json_input)
        valid = is_valid_salary_comparison(data)
        valid = data["salary_comparison"]["philippines"] < 10000 and data["salary_comparison"]["united_states"] < 10000
        return data, valid
    except (json.JSONDecodeError, TypeError) as e:
        return None, False  # Return None and False if parsing fails or keys are missing


### Functions: END


# Center the logo image
col1, col2, col3 = st.columns([2,6,2])

with col1:
    st.write(' ')

with col2:
    st.image("Connext_Logo.png", width=400) 

with col3:
    st.write(' ')

st.markdown("<h1 style='text-align: center; color: white;'>Connext Team Builder</h1>", unsafe_allow_html=True)
st.markdown("""
### Help Us Help You Find the Right Talent
Please describe the challenges, needs, or goals your company is currently facing. For example:
- Are there any specific project bottlenecks?
- What new initiatives are you planning that require additional expertise?
- Do you need recommendations for specific job roles to enhance your team's capabilities?

Provide as much detail as possible to help us suggest the most suitable job roles and expertise needed for your company. You may also input the job roles you need directly
""")

company_needs_description = st.text_area("Enter Description", height=250)

# Initialize a session state variable to store the response
if 'main_response' not in st.session_state:
    st.session_state.main_response = ""

# Initialize a session state variable to store the response
if "job_list" not in st.session_state:
    st.session_state.job_list = []

if "job_list_salary" not in st.session_state:
    st.session_state.job_list_salary = []

# Move the expander here, after the text area
with st.expander("View Response"):
    st.write(st.session_state.main_response)

if st.button("Analyze"):
    with st.spinner("Analyzing your needs..."):
        # Simulate a conversation where the assistant plays the role of an "HR talent recruiter"
        chat_log = [
            {"role": "system", "content": "You are tasked to analyze the job role needs of a company based on the description/queries from the users/company."},
            {"role": "user", "content": company_needs_description}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=chat_log
        )
        response_text = response["choices"][0]["message"]["content"]
        
        # Update the session state with the new response
        st.session_state.main_response = response_text

        #Get the job roles from the initial response
        prompt = f"""
            Based on the previous job roles analysis, can you give me the list of the job roles from the previous response and format it into a python list.
            It should just be a list of strings of the job roles.

            Example:
            ["Web Developer", "Accountant", "3D graphic artist"]
        
        """
        chat_log = [
            {"role": "system", "content": "You are an HR manager which extracts the job roles based on a user/company needs analysis."},
            {"role": "user", "content": company_needs_description},
            {"role": "assistant", "content": response_text},
            {"role": "user", "content": prompt}
        ]

        result = openai.ChatCompletion.create(
            model="gpt-4",
            messages=chat_log
        )
        job_list_response = result["choices"][0]["message"]["content"]
        job_list = extract_and_convert_list(job_list_response)
        print(job_list) #for debugging purposes
        st.session_state['job_list'] = job_list

    # Rerun the app to update the expander content
    st.rerun()

#Extract the job roles we can get from the initial response of the llm
if st.session_state['job_list']:
    job_list_salary = []

    for job in st.session_state["job_list"]:
        job_not_parsed_successfully = True

        while job_not_parsed_successfully:
            prompt = f"""
            Generate a JSON object that represents the monthly median salary in US Dollars for a specific job role, with comparisons between the Philippines and the United States. Please adhere to the following guidelines:
            - The output must be a JSON object without any comments.
            - All monetary values must be in USD.
            - Salaries should be expressed as whole numbers without commas; ensure they are realistic and below 10000.
            - Typically, salaries in the United States are significantly higher than in the Philippines; please consider this when providing figures.
            - The format of the JSON should strictly follow the structure below:
  
            
            Here's the job: {job}

            Required JSON format:
            {{
                "salary_comparison": {{
                    "philippines": <number>,
                    "united_states": <number>
                }}
            }}

            """

            chat_log = [
                {"role": "system", "content": "You are tasked to find salary information from a specific job."},
                {"role": "user", "content": prompt}
            ]

            result = openai.ChatCompletion.create(
                model="gpt-4",
                messages=chat_log
            )
            job_salary_comparison = result["choices"][0]["message"]["content"]

            print(f"Job: {job}")
            print(job_salary_comparison)

            #Extract and check if its a valid json
            salary_comparison_json, salary_comparison_parsed_successfully = extract_and_parse_json(job_salary_comparison)

            print(salary_comparison_json, salary_comparison_parsed_successfully)
            
            if salary_comparison_parsed_successfully == False:
                continue #If unsucessfull parsing was done on the salary, try again

            #Assumes it passes the if condition above
            salary_comparison_json_cleaned, salary_comparison_valid_json = validate_and_convert_salary_json(salary_comparison_json)

            print(salary_comparison_json_cleaned, salary_comparison_valid_json)

            if salary_comparison_valid_json  == False:
                continue #If invalid json parsed

            #If it passes then append to job_list_salary_then format it better:
            job_not_parsed_successfully=False #To exit the while loop
    
        #Insert the following salary comparison json to the actual json format
        job_salary = {
        "job_role": job,
         "currency": "USD",
         "salary_comparison": salary_comparison_json_cleaned['salary_comparison']
        }
        job_list_salary.append(job_salary)  # Append the formatted job salary JSON to the list
        st.session_state["job_list_salary"] = job_list_salary


    # Convert the job_list_salary into a DataFrame
    df = pd.DataFrame(job_list_salary)

    # If you want to have 'philippines' and 'united_states' as separate columns instead of nested inside 'salary_comparison':
    df = pd.concat([df.drop(['salary_comparison'], axis=1), df['salary_comparison'].apply(pd.Series)], axis=1)

    # Create columns with specific weights to center the main content
    col1, col2, col3 = st.columns([1,8,1])
    # Display the DataFrame
    with col2:
        st.dataframe(df)


#Extract the parsed job_list_salary
if st.session_state['job_list_salary']:
    total_jobs = len(st.session_state['job_list_salary'])

    st.markdown("""##### Select the number of employees you plan to hire""")

    columns_per_row = 2
    num_rows = (total_jobs + columns_per_row - 1) // columns_per_row  # Calculate number of rows needed

    for i in range(num_rows):
        cols = st.columns(columns_per_row)  # Create columns
        for j in range(columns_per_row):
            job_index = i * columns_per_row + j
            if job_index < total_jobs:  # Ensure job index is within the list range
                job = st.session_state['job_list_salary'][job_index]
                with cols[j]:  # Display widget in the specific column
                    # Create and use number input directly, tying it to the session state
                    st.session_state['job_list_salary'][job_index]["no of employees"] = st.number_input(f"{job['job_role']}:", min_value=0, key=f"num_{job['job_role']}")

if st.session_state["job_list_salary"]:
    if st.button("Caculate Cost"):
        total_jobs = len(st.session_state['job_list_salary'])

        st.markdown("""##### Cost Calculation""")

        print(f"Calculating cost... {st.session_state['job_list_salary']}")
        for i in range(total_jobs):
            st.session_state['job_list_salary'][i]["philippines_total_cost"] = st.session_state['job_list_salary'][i]["no of employees"] * st.session_state['job_list_salary'][i]["salary_comparison"]["philippines"]
            st.session_state['job_list_salary'][i]["united_states_total_cost"] = st.session_state['job_list_salary'][i]["no of employees"] * st.session_state['job_list_salary'][i]["salary_comparison"]["united_states"]
            st.session_state['job_list_salary'][i]["total_savings"] = st.session_state['job_list_salary'][i]["united_states_total_cost"] - st.session_state['job_list_salary'][i]["philippines_total_cost"]

        # Convert the job_list_salary into a DataFrame
        df = pd.DataFrame(job_list_salary)

        # If you want to have 'philippines' and 'united_states' as separate columns instead of nested inside 'salary_comparison':
        df = pd.concat([df.drop(['salary_comparison'], axis=1), df['salary_comparison'].apply(pd.Series)], axis=1)
        # Display the DataFrame
        st.dataframe(df)

        buffer = io.BytesIO()
        df.to_csv(buffer, index=False)
        st.download_button(
            label="Download data as CSV",
            data=buffer,
            file_name='team_builder_report.csv',
            mime='text/csv',
        )


        philippines_overall_cost = df["philippines_total_cost"].sum()
        united_states_overall_cost = df["united_states_total_cost"].sum()
        expected_savings = df["total_savings"].sum()

        st.write(f"Philippines Overall Cost: {philippines_overall_cost} USD")
        st.write(f"United States Overall Cost: {united_states_overall_cost} USD")
        st.divider()
        st.write(f"* If you are to hire all of your employees from the Philippines, the following is your expected savings.")
        st.write(f"Overall Savings: {expected_savings} USD")
