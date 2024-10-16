import requests
import streamlit as st

def analyze_pdf_via_api(file):
    # Send the file to the Flask backend API
    files = {"file": file}
    response = requests.post("http://127.0.0.1:5000/analyze-pdf", files=files)

    if response.status_code == 200:
        return response.json().get("result")
    else:
        st.error("Error: " + response.json().get("error", "Unknown error occurred"))
        return None

def ask_question_via_api(question):
    # Send the user question to the Flask backend API
    data = {"question": question}
    response = requests.post("http://127.0.0.1:5000/ask-question", json=data)

    if response.status_code == 200:
        return response.json().get("response")
    else:
        st.error("Error: " + response.json().get("error", "Unknown error occurred"))
        return None

# Initialize session state for messages if it doesn't exist
if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.title("Alpaca 3 - Liminal Works")

# File upload in the sidebar
df = st.sidebar.file_uploader("Upload your PDF file", type=["pdf"])
if st.sidebar.button("Analyze"):
    if df is not None:
        with st.spinner("Analyzing your PDF..."):
            response = analyze_pdf_via_api(df)
            if response:
                # Add the response to the session state messages
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Display chat messages from the session state
                for message in st.session_state.messages:
                    st.chat_message(message["role"]).markdown(message["content"])

# User question input
user_question = st.text_input("Ask a question about the Theory of Change content:")

# Button to trigger user question analysis
if st.button("Submit Question"):
    if user_question.strip() != "":
        with st.spinner("Fetching the response..."):
            response = ask_question_via_api(user_question)
            if response:
                # Add the user input and response to the session state messages if they don't already exist
                if not any(msg["content"] == user_question and msg["role"] == "user" for msg in st.session_state.messages):
                    st.session_state.messages.append({"role": "user", "content": user_question})
                
                if not any(msg["content"] == response and msg["role"] == "assistant" for msg in st.session_state.messages):
                    st.session_state.messages.append({"role": "assistant", "content": response})

# Keep the chat visible all the time
for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").markdown(f"**You:** {message['content']}")
    else:
        st.chat_message("assistant").markdown(f"**Alpaca 3:** {message['content']}")

# Add an "About" section at the bottom of the app
st.markdown("---")
st.markdown("### About")
st.markdown("Alpaca 3 is a PDF analysis tool that allows you to upload PDFs and ask questions about their content. "
            "Powered by a backend AI system, it provides insights based on the document data and your queries.")
