#This is a testing build to try how to build LLM chat app using user provided API

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_together import ChatTogether
from langchain_groq import ChatGroq
from langchain_community.chat_models import ChatHuggingFace
from langchain_anthropic import ChatAnthropic
from langchain_perplexity import ChatPerplexity

st.title("🧪 Test Streamlit Multi-LLM Chat App")

# Sidebar: choose provider
provider = st.sidebar.selectbox(
    "Choose LLM Provider:",
    ("OpenAI", "Together", "Groq", "Hugging Face", "Anthropic", "Perplexity")
)

# Sidebar: api key & optional model name
api_key = st.sidebar.text_input(f"{provider} API Key", type="password")
model_name = st.sidebar.text_input("Model name (optional)", "")

model = None

if api_key:
    try:
        if provider == "OpenAI" and api_key.startswith("sk-"):
            model = ChatOpenAI(
                api_key=api_key,
                model=model_name or "gpt-4o-mini",
                temperature=0.7
            )

        elif provider == "Together":
            model = ChatTogether(
                together_api_key=api_key,
                model=model_name or "mistralai/Mistral-7B-Instruct-v0.2",
                temperature=0.7
            )

        elif provider == "Groq":
            model = ChatGroq(
                groq_api_key=api_key,
                model_name=model_name or "llama3-8b-8192",
                temperature=0.7
            )

        elif provider == "Hugging Face":
            # Typical model e.g. "HuggingFaceH4/zephyr-7b-beta"
            model = ChatHuggingFace(
                huggingfacehub_api_token=api_key,
                repo_id=model_name or "HuggingFaceH4/zephyr-7b-beta",
                temperature=0.7
            )

        elif provider == "Anthropic" and api_key.startswith("sk-ant-"):
            model = ChatAnthropic(
                anthropic_api_key=api_key,
                model_name=model_name or "claude-3-haiku-20240307",
                temperature=0.7
            )

        elif provider == "Perplexity" and api_key.startswith("pplx-"):
            model = ChatPerplexity(
                perplexity_api_key=api_key,
                model=model_name or "pplx-7b-online",
                temperature=0.7
            )
        else:
            st.error("Unsupported provider or invalid API key format.")
    except Exception as e:
        st.error(f"Error initializing model: {e}")

if model:
    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])
    
    # Chat input at the bottom
    user_input = st.chat_input("Type your question...")
    if user_input:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        try:
            # Call the model
            response = model.invoke(user_input)
            assistant_reply = response.content

            # Add assistant reply to history
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
            st.chat_message("assistant").write(assistant_reply)
        except Exception as e:
            st.error(f"Error calling model: {e}")
else:
    st.warning("Please enter your API key and choose a provider.", icon="⚠")
