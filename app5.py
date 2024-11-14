import streamlit as st
from openai import OpenAI
import yaml

client = OpenAI(
    api_key="api-key"
)

# Load YAML logic data
logic_yaml = """
title: "AI Model Logic Draft"
packages:
  - package: "Foundation Package"
    price: "£99"
    ideal_for: "Early job search stages"
    criteria:
      applications_submitted: "0-5"
      interviews_received: "0-1"
      confidence_in_strategy: "Neutral to Not Confident"
    services:
      - "CV, Cover Letter, and LinkedIn Review"
      - "One Free Consulting Call"
      - "3 ATS-Friendly Resumes and Cover Letters"

  - package: "Advanced Package"
    price: "£149"
    ideal_for: "Moderate engagement, lacking interview success"
    criteria:
      applications_submitted: "6-10"
      interviews_received: "1-2"
      confidence_in_strategy: "Neutral"
    services:
      - "All Services in the Foundation Package"
      - "Personalized Interview Answers"
      - "Weekly Job Subscription"
      - "Subscription Bundle"

  - package: "Professional Package"
    price: "£249"
    ideal_for: "Some UK experience, needs project-based work"
    criteria:
      applications_submitted: "11-20+"
      interviews_received: "3-5"
      relevance_of_experience: "Somewhat to Highly Relevant"
      confidence: "Neutral"
    services:
      - "All the services in the Advanced Package and Foundation Package"
      - "Mentorship Session"
      - "Project-Based Experience"
      - "Mock Interview Prep"
      - "Career Fairs and Networking"
      - "Events Updates"

  - package: "Ultimate Career Package"
    price: "£399"
    ideal_for: "Near visa expiration, seeking internships/certifications"
    criteria:
      applications_submitted: "21+"
      interviews_received: "6+"
      visa_expiry: "Less than 6 months"
    services: 
      - "All the services in the Advanced Package, Foundation Package and Professional Package"
      - "Internship"
      - "1 Interview with company in selected domain"
      - "Certification training and guidance"
"""
logic_data = yaml.safe_load(logic_yaml)

# Function to ask questions and get user input
def get_user_input():
    form_data = {}

    # Asking user's name and email
    form_data['name'] = st.text_input("Please enter your name:")
    form_data['email'] = st.text_input("Please enter your email:")

    # Asking job search-related questions
    form_data['applications_submitted'] = st.number_input("How many job applications have you submitted so far?", min_value=0, step=1)
    form_data['interviews_received'] = st.number_input("How many interviews have you been invited to in the UK?", min_value=0, step=1)
    form_data['confidence_level'] = st.selectbox("How confident are you in your job search strategy?", ["Very Confident", "Confident", "Neutral", "Not Confident"])
    form_data['work_experience_uk'] = st.selectbox("How relevant is your work experience in the UK to your desired career path?", ["Highly Relevant", "Somewhat Relevant", "Not Relevant"])
    form_data['psw_visa'] = st.text_input("Do you currently hold a Post-Study Work (PSW) visa?")
    form_data['visa_expiry_months'] = st.number_input("How many months are left on your current visa before it expires?", min_value=0, step=1)
    form_data['phone_number'] = st.text_input("Phone number",)
    form_data['linkedin'] = st.text_input("LinkedIn Profile URL")
    form_data['course'] = st.text_input("What is your current course of study in the UK?")
    form_data['highest_education'] = st.text_input("What is your highest level of education completed prior to this course?")
    form_data['work_experience_in_home_country'] = st.text_input("How many years of work experience do you have in your home country?")
    form_data['Have_you_started_applying_for_jobs_in_the_UK?'] = st.text_input("Have you started applying for jobs in the UK?")
    form_data['uk_experience'] = st.text_input("Have you gained any work experience in the UK (internships, part-time jobs, etc.)?")
    form_data['uk_experience_type'] = st.text_input("If yes, please describe the type of work experience you have gained in the UK.")
    form_data['relevant'] = st.text_input("How relevant is this experience to your desired career path?")
    form_data['target_indusrty'] = st.text_input("What type of job or industry are you targeting in the UK?")
    form_data['identified_companies_organizations_in_UK_where_you_would_like_to_work'] = st.text_input("Have you identified companies or organizations in the UK where you would like to work?")
    form_data['companies_your_looking_for'] = st.text_input("If yes, please list the top three companies or organizations.")
    form_data['search_methods_currently_using'] = st.text_input("What job search methods are you currently using?")
    form_data['how_confident_in_job_search_startegy'] = st.text_input("How confident are you in your job search strategy?")
    form_data['aware_of_visa_req'] = st.text_input("Are you aware of the visa requirements for working in the UK after your PSW visa expires?")
    form_data['explored_visa_option_for_staying_in_uk'] = st.text_input("Have you started exploring visa options for staying in the UK beyond your current visa?")
    form_data['receiving_support_for_job_search_from_university_or_organizations?'] = st.text_input("Are you receiving any support for your job search from your university or other organizations? ")
    form_data['kind_of_support_you_received'] = st.text_input("If yes, what kind of support are you receiving?")
    form_data['additional_resources_or_support_think_would_help_you'] = st.text_input("What additional resources or support do you think would help you in your job search?")
    form_data['biggest_barriers_to_finding_job_in_the_UK'] = st.text_input("What do you perceive as the biggest barriers to finding a job in the UK?   ")
    form_data['What_immediate_next_steps_in_your_job_search'] = st.text_input("What are your immediate next steps in your job search?")
    form_data['plan_if_you_are_unable_to_secure_a_job'] = st.text_input("Do you have a plan if you are unable to secure a job before your visa expires?")
    form_data['backup_plan'] = st.text_input("If yes, what is your backup plan?")
    

    return form_data

def recommend_package_openai(form_data, logic_data):
    prompt = f"""
    Given the following job search profile for a user named {form_data['name']}:
    - Applications Submitted: {form_data['applications_submitted']}
    - Interviews Received: {form_data['interviews_received']}
    - Confidence Level: {form_data['confidence_level']}
    - Work Experience Relevance: {form_data['work_experience_uk']}
    - Visa Expiry Months: {form_data['visa_expiry_months']}
    
    Choose the most suitable package from the available options below and return only the package name and its price in the 1st line:
    "Package Name for £Price"
    
    Available Packages:
    {logic_data}
    
    Provide the recommended package name and reasoning for the choice. mention the points which which makes this package a good fit.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in career counseling."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    return response.choices[0].message.content


def get_reasoning(package, form_data):
    prompt = f"The user named {form_data['name']} has provided the following job search details: \n"
    prompt += f"- Applications Submitted: {form_data['applications_submitted']}\n"
    prompt += f"- Interviews Received: {form_data['interviews_received']}\n"
    prompt += f"- Confidence Level: {form_data['confidence_level']}\n"
    prompt += f"- Work Experience Relevance: {form_data['work_experience_uk']}\n"
    prompt += f"- Visa Expiry Months: {form_data['visa_expiry_months']}\n"
    prompt += f"\nBased on the above information, the recommended package is {package}. Please provide a comprehensive reasoning for why this package is the best fit for the user. write package and only Price in first line."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    # print(response)
    return response.choices[0].message.content


def main():
    st.title("Assesment")
    form_data = get_user_input()

    if st.button("Get Recommended Package"):
        if form_data['name'] and form_data['email']:
            recommendation = recommend_package_openai(form_data, logic_yaml)
            # Assuming the response from OpenAI starts with the package name
            # Separate the package name and reasoning for display
            lines = recommendation.splitlines()
            package_name = lines[0] if lines else "Package Recommendation"
            reasoning = "\n".join(lines[1:]) if len(lines) > 1 else "No reasoning provided."

            st.subheader(f"Recommended Package: {package_name}")
            st.write(reasoning)
        else:
            st.warning("Please enter your name and email before proceeding.")


if __name__ == "__main__":
    main()

