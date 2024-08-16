## Frontend UI App (to be developed by the Frontend Engineering team)

# Import Streamlit for creating the frontend UI
import streamlit as st
from model import *  # Import the ChatBot class from model.py
import requests      # Import requests for making API calls to the backend

# Instantiate the ChatBot class
chat_bot = ChatBot()

# Initialize session state to keep track of user inputs and responses across interactions
if 'responses' not in st.session_state:
    st.session_state.responses = []

# Set the model and temperature (creativity level) for the LLM
selected_model = chat_bot.models[0]  # Use the first model in the list (default)
temperature = 0.2                    # Set a moderately creative response level

# Define the backend API URL that will handle the chatbot's responses
backend_url = "http://127.0.0.1:5000/chat_batch"  # Local FastAPI server

# Function to handle user input and retrieve responses from the backend API
def handle_message(user_input):
    if user_input:
        # Add the user's input to the session state for tracking
        st.session_state.responses.append({'user': user_input, 'bot': None})
        
        # Create an empty container to update the response in real-time
        response_container = st.empty()

        # Make a POST request to the backend API with the user's input
        response = requests.post(backend_url, json={"message": user_input, "model": selected_model, "temperature": temperature}, stream=True)

        # Check if the response is successful
        if response.status_code == 200:
            bot_response = ""
            
            # Process the response in chunks (streaming mode), iter_content method iterates over the response data 
            for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                bot_response += chunk
            
            # Display the bot's response in a styled box on the UI
            st.markdown(f"""
            <div style="background-color:#f0f0f0; padding:10px; border-radius:5px;">
                <p style="font-family:Arial, sans-serif;">{bot_response.strip()}</p>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            # If the API call fails, show an error message
            response_container.markdown("<p style='color:red;'>Error: Unable to get a response from the server.</p>", unsafe_allow_html=True)

        # Clear the input box after sending the message
        st.session_state.current_input = ""

# Create an input text box for the user to type their query
if 'current_input' not in st.session_state:
    st.session_state.current_input = ""
user_input = st.text_input("You:", st.session_state.current_input)

# Add a button that sends the user's input to the backend when clicked
if st.button("Send"):
    handle_message(user_input)
