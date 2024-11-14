import streamlit as st
import time
import random

# side bar setup
with st.sidebar:
    st.markdown("An ML Bot Built with Gemini.")
    st.caption("Kean Teng © 2024")

# main page
st.title("⚡ML Bot")

# backend functions

# chat section
# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.06)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("How can ML Bot help you today?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user", avatar="https://64.media.tumblr.com/7b526ba246f48e294ebc87fe2cbd8e1b/1a4bdb8275a18adc-c7/s500x750/8f2e5c09cb5513c23798349c7c68013248f0b912.jpg"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcThr7qrIazsvZwJuw-uZCtLzIjaAyVW_ZrlEQ&s"):
        with st.status("Thinking ...", expanded=True) as status:
            st.write("Searching for information...")
            time.sleep(2)
            status.update(
                label="Memory Updated", state="complete", expanded=False
            )
        response = st.write_stream(response_generator())
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})