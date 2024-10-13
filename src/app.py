import os
import json

from openai import OpenAI
import streamlit as st


#set page title
st.title("Alpaca 3")


#config api key
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))
client = OpenAI(
    api_key = config_data["OPENAI_API_KEY"]
)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

print(st.session_state["openai_model"])  # Debugging

#initialize chat session if no previous session exists
if "messages" not in st.session_state:
    st.session_state.messages = []

#display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#take user input
if user_input := st.chat_input("Enter message:"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)


    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        result = ""
        full_response = ""
        
        #openai.chat.completion.create
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            
        #full_response += response.choices[0].delta.get("content", "")
            result = response.choices[0].delta.content
            if(isinstance(result, str)):
                full_response += result
            
            message_placeholder.markdown(full_response + "▌")

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response})
            
    message_placeholder.markdown(full_response)


