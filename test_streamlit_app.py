import streamlit as st
from langchain_openai import ChatOpenAI

st.title("Test Streamlit LLM Chat App")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")


if openai_api_key and openai_api_key.startswith("sk-"):
    model = ChatOpenAI(temperature=0.7, api_key=openai_api_key)

    def generate_response(input_text):
        response = model.invoke(input_text)
        st.info(response)
    
    with st.form("my_form"):
        text = st.text_area(
            "Enter text:",
            "What are the three key pieces of advice for learning how to code?",
        )
        submitted = st.form_submit_button("Submit")
        if submitted:
            generate_response(text)
else:
    st.warning("Please enter your OpenAI API key!", icon="⚠")
