import logging
import streamlit as st
import pymupdf
from langchain.chains.question_answering import load_qa_chain
from langchain_groq import ChatGroq
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate


logging.basicConfig(level=logging.DEBUG)


# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    logging.info("Extracting text from pdf file.")
    pdf_file.seek(0)  # Reset file pointer to the beginning
    pdf_bytes = pdf_file.read()
    pdf_reader = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in pdf_reader:
        text += page.get_text()
    return text

# Function to create Langchain document objects from PDF text
def create_documents_from_texts(text):
    return [Document(page_content=text)]


def main():
    st.set_page_config(page_title="PDF Question Answering Application")


    # Hide Streamlit style elements (top-right menu, footer, and deploy button)
    hide_streamlit_style = """
                <style>
                /* Hide Streamlit header */
                header {visibility: hidden;}

                /* Alternatively, hide specific elements within the header */
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}

                /* Hide the deploy button */
                .viewerBadge_container__1QSob {display: none !important;}

                /* Hide the status widget */
                .stStatusWidget {display: none !important;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    st.title("PDF QA Demo")

    uploaded_files = st.file_uploader("Upload PDF Files", type=["pdf"], accept_multiple_files=True)
    
    if uploaded_files:
        pdf_text = ""
        for uploaded_file in uploaded_files:
            pdf_text += extract_text_from_pdf(uploaded_file)
        
        # st.text_area("Extracted PDF Text", pdf_text, height=300)

        documents = create_documents_from_texts(pdf_text)

        prompt_template = """
            You are a helpful assistant. Use the following context to answer the question at the end. 
            If the answer cannot be found within the context, respond with:
            'The information you are looking for was not found in the provided PDF.'

            Context: {context}

            Question: {question}
            """
        
        # Allow the user to ask questions
        question = st.text_input("Ask a question based on the PDF content:")
        
        # if question and st.button("Get Answer"):
        if question:
            llm = ChatGroq(
                model="llama-3.1-8b-instant",
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2,
                # other params...
            )

            qa_prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

            chain = load_qa_chain(llm, chain_type="stuff", prompt=qa_prompt)
            
            # Run the chain and get the answer
            result = chain.run(input_documents=documents, question=question)
            
            st.write("Answer:", result)

if __name__ == "__main__":
    main()
