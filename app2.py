import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key="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"
)

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
    form_data['visa_expiry_months'] = st.number_input("How many months are left on your current visa before it expires?", min_value=0, step=1)

    return form_data

# Function to recommend package based on user input
def recommend_package(form_data):
    if form_data.get('applications_submitted') <= 5 and form_data.get('interviews_received') <= 1 and form_data.get('confidence_level') in ['Neutral', 'Not Confident']:
        return "Foundation Package (£99)"

    elif 6 <= form_data.get('applications_submitted') <= 10 and 1 <= form_data.get('interviews_received') <= 2:
        return "Advanced Package (£149)"

    elif 11 <= form_data.get('applications_submitted') <= 20 and 3 <= form_data.get('interviews_received') <= 5:
        if form_data.get('work_experience_uk') in ['Somewhat Relevant', 'Highly Relevant']:
            return "Professional Package (£249)"

    elif form_data.get('applications_submitted') > 20 and form_data.get('interviews_received') > 5:
        if form_data.get('visa_expiry_months') and form_data.get('visa_expiry_months') < 6:
            return "Ultimate Career Package (£399)"


    return "Foundation Package (£99)"


def get_reasoning(package, form_data):
    prompt = f"The user named {form_data['name']} has provided the following job search details: \n"
    prompt += f"- Applications Submitted: {form_data['applications_submitted']}\n"
    prompt += f"- Interviews Received: {form_data['interviews_received']}\n"
    prompt += f"- Confidence Level: {form_data['confidence_level']}\n"
    prompt += f"- Work Experience Relevance: {form_data['work_experience_uk']}\n"
    prompt += f"- Visa Expiry Months: {form_data['visa_expiry_months']}\n"
    prompt += f"\nBased on the above information, the recommended package is {package}. Please provide a comprehensive reasoning for why this package is the best fit for the user."

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
    st.title("UK Job Search Package Recommender")
    form_data = get_user_input()

    if st.button("Get Recommended Package"):
        if form_data['name'] and form_data['email']:
            recommended_package = recommend_package(form_data)
            reasoning = get_reasoning(recommended_package, form_data)
            st.subheader(f"Recommended Package: {recommended_package}")
            st.write(reasoning)
        else:
            st.warning("Please enter your name and email before proceeding.")


if __name__ == "__main__":
    main()

