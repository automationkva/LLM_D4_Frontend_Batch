## Backend App/Server App (to be developed by the Backend Engineering team)

# Import necessary modules and classes
from model import ChatBot                    # Import the ChatBot class from model.py
from fastapi import FastAPI, Request, HTTPException  # Import FastAPI, Request object, and HTTPException handling
from fastapi.responses import StreamingResponse, PlainTextResponse  # Import response types from FastAPI
from dotenv import load_dotenv              # Import dotenv to load environment variables
import traceback                            # Import traceback for detailed error logging

# Load environment variables from the .env file
load_dotenv()

# Initialize the FastAPI app
app = FastAPI()

# Instantiate the ChatBot class to create a chatbot object
chatbot = ChatBot()

# Access the Groq client through the chatbot object
client = chatbot.client

# Define a POST route to handle chat requests in batch mode
@app.route("/chat_batch", methods=["POST"])
async def chat_batch(request: Request):
    """
    Handles incoming POST requests to the /chat_batch endpoint.
    
    Parameters:
        request (Request): The incoming HTTP request object containing user input.
    
    Returns:
        PlainTextResponse: The generated response from the chatbot or an error message.
    """
    # Parse the incoming JSON request body
    user_input = await request.json()  # Extract JSON data from the request asynchronously
    user_message = user_input.get("message")  # Get the user's message from the JSON payload
    temperature = float(user_input.get("temperature"))  # Get the temperature setting for response creativity
    selected_model = user_input.get("model")  # Get the selected model from the user input
    
    try:
        # Generate a response using the chatbot's batch response method
        response = chatbot.get_response_batch(message=user_message, temperature=temperature, model=selected_model)
        
        # Extract the content of the response
        output = response.choices[0].message.content
        
        # Return the response as plain text with a 200 OK status
        return PlainTextResponse(content=output, status_code=200)
    
    except Exception as e:
        # If an error occurs, log the detailed traceback and return an error message
        print(traceback.format_exc())
        return {
            "error": str(e),
            "status_code": 400  # Returning 400 so that even when we know something is wrong, yet we avoid breaking client-side code and exit gracefully/orderly.
        }
