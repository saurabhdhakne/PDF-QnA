import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key="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"
)


def get_user_input():
    form_data = {}

    # Asking user's name and email
    form_data['text'] = st.text_input("Please enter your details")
    return form_data

def recommend_package(form_data):
    
    return

def main():
    st.title("UK Job Search Package Recommender")
    form_data = get_user_input()

    if st.button("Get Recommended Package"):
        if form_data['text']:
            recommended_package = recommend_package(form_data)
            st.subheader(f"Recommended Package: {recommended_package}")
            st.write(recommended_package)
        else:
            st.warning("Please enter your name and email before proceeding.")