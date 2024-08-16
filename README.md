## Initial Setup
```
1. Run ```python -m venv .venv``` to create a python virtual environment
2. Run ```.venv\Scripts\activate``` to activate the virtual environment
3. Create requirements.txt file and add all the dependencies
4. Run ```pip install -r requirements.txt``` to install dependencies
    [When updated later, run ```pip freeze > requirements.txt``` to update dependencies]
5. 
```

## Project Overview
```
This project is a simple chatbot application built using Python, which integrates FastAPI for the backend and Streamlit for the frontend. The chatbot uses a language model from Groq to generate responses based on user input. The application is structured to allow interaction with the chatbot through both a web-based frontend (via Streamlit) and an API (via FastAPI). The overall flow of the end-to-end journey is as follows:
1. User Input (Frontend - main.py) → User sends input through Streamlit.
2. API Call (Frontend - main.py) → Request is sent to the FastAPI backend (app.py).
3. Request Handling (Backend - app.py) → Backend receives the request and parses it.
4. Chatbot Logic (Model - model.py) → Chatbot processes the input, interacts with the Groq API, and generates a response.
5. Response Handling (Backend - app.py) → Backend processes and formats the chatbot response.
6. Display Response (Frontend - main.py) → Frontend receives and displays the response to the user.
```

## Application Components
```
1. Model (model.py):
Encapsulates the logic for interacting with the Groq API. This file defines the ChatBot class, which handles generating responses from the language model. The ChatBot class has methods to handle both real-time streaming responses and batch responses from the model, depending on how the frontend or backend calls it.

2. Backend (app.py):
Handles the API requests and responses. It acts as the core server-side logic of the application, interacting with the language model through the ChatBot class (from model.py).
app.py is the backend entry point where the FastAPI server is set up, and the /chat_batch route is defined for handling POST requests. When a POST request is made to the /chat_batch endpoint, the backend receives the user's message, processes it using the language model, and returns the generated response as plain text.

3. Frontend (main.py):
Provides the user interface using Streamlit, which allows users to interact with the chatbot via a web page.
main.py is the frontend entry point. It contains the code that runs the Streamlit application, displaying the chatbot UI. Users enter their queries into a text box, and when they press "Send," the input is sent to the backend API (/chat_batch) for processing. The bot's response is then displayed on the web page.

4. Dependencies (requirements.txt):
Lists all the necessary Python packages required to run the project. This includes groq for the language model, fastapi for the API backend, streamlit for the frontend, and uvicorn to serve the FastAPI application.
```

## Implementation Structure
```
1. Create the model (model.py):
- Start by implementing the core chatbot logic that interacts with the Groq API.

2. Build the backend (app.py):
- Set up FastAPI to handle requests and call the chatbot model. Define routes for handling chat messages.

3. Develop the frontend (main.py):
- Implement the Streamlit interface for users to interact with the chatbot.

4. Set up dependencies (requirements.txt):
- List all the required packages for easy installation and environment setup.

5. Configure environment variables (.env):
- Store sensitive information like API keys in the .env file.

6. Add sensitive file to .gitignore:
- Add the .env and other sensitive files to .gitignore to prevent them from being committed to version control

7. Setup Source Control (Git):
- Initialize a Git repository and commit your code regularly.
```

## Solution Architecture
This explains the overall workflow from transaction origination to completion.
1. User Interaction (Streamlit Web UI - main.py):
- The journey begins when a user inputs a query through the text input box on the Streamlit interface and clicks the "Send" button.
- If the session state is not initialized, ```main.py``` initializes it to store the responses from the chatbot.
- The ```main.py``` script pre-selects the model ```(selected_model = chat_bot.models[0])``` and sets the temperature parameter ```(temperature = 1.5)```.
- Upon clicking "Send," the ```handle_message()``` function is triggered. This function sends a POST request to the backend API ```(backend_url = "http://127.0.0.1:5000/chat_batch")``` with the user's input (user_input), selected model, and temperature parameters in the JSON payload.
- The ```requests.post()``` function sends the input to the backend and waits for a response. If the response is successful, the ```iter_content()``` method is used to iterate over the content and handle the response in real-time, displaying the chatbot's response to the user as it is received, allowing for a streaming-like interaction.

2. Backend Request Handling (FastAPI - app.py):
- The POST request sent by the Streamlit frontend is received by the ```/chat_batch``` endpoint defined in app.py.
- app.py parses the incoming JSON payload using ```request.json()```, extracting the message (user input), temperature, and model.
- After extracting the required parameters, app.py calls the ```get_response_batch()``` method of the ChatBot class from model.py. This method handles the logic for interacting with the Groq API.

3. Chatbot Logic (Model - model.py):
- Inside the ```get_response_batch()``` method, the chatbot interacts with the Groq API to generate a response based on the user input, system prompt, and selected model. The API call is made using the ```client.chat.completions.create()``` method, passing the user input, model, and temperature as parameters.
- The Groq API returns a response containing the chatbot’s generated answer. This response is structured as a batch, containing text data.
- The model.py returns the chatbot’s response (processed text) back to app.py.

4. Backend Response Handling (FastAPI - app.py):
- Once app.py receives the chatbot’s response from model.py, it extracts the content (text output) from the API response. If the response is successful, it sends this content back to the frontend as a plain text response (PlainTextResponse).
- If an error occurs during the processing of the user input or the API call, app.py captures the error, logs it, and sends an error message back to the frontend.

5. Frontend Displays Response (Streamlit Web UI - main.py):
- After sending the request to the backend, main.py receives the chatbot’s response. The response is handled in chunks (via response.iter_content()) to simulate streaming.
- The response is formatted in HTML using Streamlit's ```st.markdown()``` method and displayed to the user in a styled container. The input box is then cleared for the next user query.

6. Continuous Interaction:
The user can continue to interact with the chatbot by inputting additional queries. Each interaction follows the same flow, with the state maintained through Streamlit's session state to track previous responses.


## Running the Project in Development
Start the FastAPI server with uvicorn, and run the Streamlit app. Test using the Streamlit UI or Postman.
- Start the Backend:
Run the command ```uvicorn app:app --host 127.0.0.1 --port 5000 --reload```.
This starts the FastAPI backend server on localhost:5000.
- Start the Frontend:
Run the command ```streamlit run main.py```.
This starts the Streamlit application, which will open a web interface in the browser.

## Deployment to Production
```
Create a Dockerfile to containerize the application for consistent deployment across environments.

- Backend: Deploy the FastAPI backend to a cloud server (like AWS, Azure, GCP, Heroku) using Docker, or run it with a production-ready server like 'gunicorn' or 'uvicorn'.

- Frontend: Deploy the Streamlit frontend using Streamlit Sharing or any other web hosting platform that supports Python web apps.

This code setup enables a seamless interaction between the frontend and backend, allowing users to interact with the chatbot while the backend handles the heavy lifting of generating responses via the Groq API.
```

## Other Project Information
