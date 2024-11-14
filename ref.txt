import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from sklearn.linear_model import LinearRegression
import numpy as np

# Load environment variables from .env file
load_dotenv()

# Access the API token
api_key = os.getenv('API_TOKEN')
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize a sample prediction model
sample_model = LinearRegression()
# Sample training data
X_train = np.array([[1], [2], [3], [4], [5]])
y_train = np.array([1, 4, 9, 16, 25])
sample_model.fit(X_train, y_train)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Function to get response from Gemini
def get_gemini_response(user_input):
    response = model.generate_content(user_input)
    return response.text

# Function to get prediction
def get_prediction(input_details):
    # Convert input details to numpy array for prediction
    input_array = np.array([[float(input_details)]])
    prediction = sample_model.predict(input_array)
    return prediction[0]

# Chat interface
st.title("Chat with Gemini 1.5 Flash")

st.title("Chat with Gemini 1.5 Flash")

# Initialize session state if not already done
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Create a placeholder for the chat history
chat_history_placeholder = st.empty()

# Function to update chat history
def update_chat_history():
    with chat_history_placeholder.container():
        for message in st.session_state['messages']:
            st.write(f"**{message['role']}**: {message['content']}")

# Display the initial chat history
update_chat_history()

# Chat input
user_input = st.text_input("You:", key="user_input")
if user_input:
    st.session_state['messages'].append({"role": "User", "content": user_input})

    # Check if user requests a prediction
    if 'prediction' in user_input.lower():
        st.write("Please provide details for prediction:")
        with st.form("prediction_form"):
            input_details = st.text_input("Enter a number:")
            submitted = st.form_submit_button("Submit")
            if submitted:
                prediction_result = get_prediction(input_details)
                prediction_message = f"The prediction result for the input {input_details} is {prediction_result}."
                st.session_state['messages'].append({"role": "Assistant", "content": prediction_message})
                
                # Relay the prediction result to Gemini
                gemini_response = get_gemini_response(prediction_message)
                st.session_state['messages'].append({"role": "Assistant", "content": gemini_response})
                st.write(f"Gemini Response: {gemini_response}")
    else:
        # Get response from Gemini
        assistant_response = get_gemini_response(user_input)
        st.session_state['messages'].append({"role": "Assistant", "content": assistant_response})

    # Update the chat history after adding the new message
    update_chat_history()