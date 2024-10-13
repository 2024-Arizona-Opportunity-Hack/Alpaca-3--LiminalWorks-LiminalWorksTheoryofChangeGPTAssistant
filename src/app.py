import os
import json

import openai
import streamlit as st

#set page title
st.title("Alpaca 3")


#config api key
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))
openai.api_key = config_data["OPENAI_API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

print(st.session_state["openai_model"])  # Debugging

#initialize chat session if no previous session exists
if "message_history" not in st.session_state:
    st.session_state.message_history = []

#display chat history
for message in st.session_state.message_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#take user input
if user_input := st.chat_input("Enter message:"):
    st.session_state.message_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            message_history=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.message_history
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.message_history.append(
        {"role": "assistant", "content": full_response})
