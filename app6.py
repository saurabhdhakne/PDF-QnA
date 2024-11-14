import streamlit as st
from openai import OpenAI
import yaml

client = OpenAI(
    api_key=""
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

     # Personal and contact information
    form_data['name'] = st.text_input("Full Name")
    form_data['email'] = st.text_input("Email Address")
    form_data['phone_number'] = st.text_input("Phone Number")
    form_data['linkedin_profile'] = st.text_input("LinkedIn Profile URL")

    # Educational background and visa status
    form_data['current_course'] = st.text_input("Current Course of Study in the UK")
    form_data['highest_education'] = st.text_input("Highest Level of Education Completed")
    form_data['work_experience_home_country'] = st.text_input("Years of Work Experience in Home Country")
    form_data['psw_visa_status'] = st.text_input("Do you hold a Post-Study Work (PSW) visa? (Yes/No)")
    form_data['visa_expiry_months'] = st.number_input("Months Remaining on Current Visa", min_value=0, step=1)

    # Job search activity and confidence
    form_data['applications_submitted'] = st.number_input("Number of Job Applications Submitted in the UK", min_value=0, step=1)
    form_data['interviews_received'] = st.number_input("Number of Interviews Received in the UK", min_value=0, step=1)
    form_data['confidence_level'] = st.selectbox("Confidence Level in Job Search Strategy", ["Very Confident", "Confident", "Neutral", "Not Confident"])
    form_data['work_experience_uk_relevance'] = st.selectbox("Relevance of UK Work Experience to Desired Career Path", ["Highly Relevant", "Somewhat Relevant", "Not Relevant"])

    # Additional information for better package recommendations
    form_data['uk_job_search_started'] = st.radio("Have you started applying for jobs in the UK?", ["Yes", "No"])
    form_data['uk_experience'] = st.text_area("Describe any UK-based work experience (e.g., internships, part-time jobs)", "N/A if none")
    form_data['target_industry'] = st.text_input("Target Job or Industry in the UK")
    form_data['identified_companies'] = st.text_area("List any identified companies or organizations in the UK where you'd like to work (optional)", "N/A if none")
    form_data['current_search_methods'] = st.text_area("Current Job Search Methods (e.g., online platforms, networking, university support)")
    form_data['visa_awareness'] = st.radio("Are you aware of the visa requirements for working in the UK after PSW visa expiration?", ["Yes", "No"])
    form_data['explored_visa_options'] = st.radio("Have you explored visa options to stay in the UK beyond your current visa?", ["Yes", "No"])
    form_data['support_received'] = st.text_area("Are you receiving any job search support from your university or organizations? Describe if applicable", "N/A if none")
    form_data['additional_resources_needed'] = st.text_area("Additional Resources or Support Needed for Job Search")
    form_data['job_search_barriers'] = st.text_area("Perceived Barriers to Finding a Job in the UK")
    form_data['immediate_job_search_steps'] = st.text_area("Immediate Next Steps in Your Job Search")
    form_data['backup_plan'] = st.text_area("Plan if Unable to Secure a Job Before Visa Expiration (optional)")

    return form_data

def recommend_package_openai(form_data, logic_data):
    prompt = f"""
    Based on the following job search profile for a user named {form_data['name']}, recommend the most suitable package.
    User Profile:
    - Name: {form_data['name']}
    - Email: {form_data['email']}
    """

    # Add optional fields if they are not empty or null
    optional_fields = {
        "Current Course of Study": form_data.get("current_course"),
        "Highest Education Level Completed": form_data.get("highest_education"),
        "Work Experience in Home Country": form_data.get("work_experience_in_home_country"),
        "Applications Submitted": form_data.get("applications_submitted"),
        "Interviews Received": form_data.get("interviews_received"),
        "Confidence in Job Search Strategy": form_data.get("confidence_level"),
        "Relevant UK Work Experience": form_data.get("work_experience_uk"),
        "Type of UK Work Experience": form_data.get("uk_experience_type"),
        "Target Industry/Job Type in the UK": form_data.get("target_industry"),
        "Desired Companies/Organizations": form_data.get("identified_companies_organizations_in_UK_where_you_would_like_to_work"),
        "Job Search Methods Used": form_data.get("search_methods_currently_using"),
        "Visa Status": form_data.get("psw_visa"),
        "Visa Expiry in Months": form_data.get("visa_expiry_months"),
        "Awareness of Post-PSW Visa Requirements": form_data.get("aware_of_visa_req"),
        "Support from University or Other Organizations": form_data.get("receiving_support_for_job_search_from_university_or_organizations?"),
        "Additional Job Search Support Needed": form_data.get("additional_resources_or_support_think_would_help_you"),
        "Biggest Barriers to Finding a Job": form_data.get("biggest_barriers_to_finding_job_in_the_UK"),
        "Immediate Next Steps in Job Search": form_data.get("What_immediate_next_steps_in_your_job_search"),
        "Backup Plan if Unable to Secure Job": form_data.get("backup_plan")
    }

# Append only non-empty optional fields to the prompt
    for field_name, value in optional_fields.items():
        if value:
            prompt += f"- {field_name}: {value}\n"

    # Add the available packages and instructions for the recommendation
    prompt += f"""
    Based on this information, recommend the best package from the options below, and provide a summary explaining why this package is the best fit for the user. 

    Available Packages:
    {logic_data}
    
    Before the package recommendation, Use the user's profile data to create tailored tips that can improve their job search strategy and outcomes. List these under the title 'Job Search Improvement Tips' with bullet points for easy reference.

    Format the response to begin with the recommended package in this format:
    "Package Name for £Price"

    Then provide a detailed reasoning based on the user's job search details, highlighting the specific factors with pointers that make this package a good match.
    
    Finally, assess the likelihood for each package by distributing percentages across all available packages, with the total summing to 100%. Assign a percentage to each package based on how well it meets the user's needs and list each package with its percentage on a new line, formatted as:
    "Package Name: X%"
    
    """

    print("Final prompt")
    print(prompt)
    
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
        max_tokens=1000
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

            st.subheader(f"{package_name}")
            st.write(reasoning)
        else:
            st.warning("Please enter your name and email before proceeding.")


if __name__ == "__main__":
    main()

