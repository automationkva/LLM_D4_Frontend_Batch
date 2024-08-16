## Backend model accessed via Groq API (will be developed by the DS/ML team)

import os
import groq
from dotenv import load_dotenv

# Load environment variables from a .env file, typically used for API keys and other secrets
load_dotenv()

class ChatBot():
    """
    This class handles the interaction with the language model (LLM)
    using the Groq API. It defines methods to generate responses
    based on user input.
    """
    
    # Load the Groq API key from environment variables
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    
    # Initialize the Groq API client with the API key
    client = groq.Groq(api_key=GROQ_API_KEY)
    
    # Initialize variables for user query and output
    query: str
    output: str = ""
    
    # Define a list of available models. Each model has different capabilities.
    models = [
        # "llama-3.1-405b-reasoning",  # Uncomment this if you need more advanced reasoning
        "llama-3.1-70b-versatile",    # Default versatile model
        "llama-3.1-8b-instant",       # Faster, smaller model for instant responses
        "mixtral-8x7b-32768"          # Another available model option
    ]
    
    # Define output types, Stream mode provides a continuous flow of responses, while Batch mode processes all at once
    output_type = ["Stream", "Batch"]
    
    # Define a system prompt that guides the LLM's responses
    sys_prompt = """
        You are an intelligent generative search assistant. 
        As an expert trained on a diverse knowledge base, 
        provide the best possible response to my query 
        using the most recent information.
    """
    
    def get_response(self, message, model="llama-3.1-70b-versatile", temperature=0):
        """
        Generates a response using the LLM in Stream mode.
        
        Parameters:
            message (str): The user input message/query.
            model (str): The model to use for generating the response.
            temperature (float): Controls the randomness of the response (0 for deterministic, higher for more creative).
        
        Returns:
            response: The response object from the Groq API, or an error message.
        """
        try:
            # Request the LLM to generate a response in Stream mode
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": f"{self.sys_prompt}"},  # Add system prompt
                    {"role": "user", "content": f"{message}"}             # Add user query
                ],
                stream=True,              # Stream mode for continuous response
                temperature=temperature,  # Temperature for response creativity
                max_tokens=1536,          # Limit the response length to 1536 tokens
            )
            return response
        
        except Exception as e:
            # Handle any errors that occur during the API call
            return {"error": str(e)}

    def get_response_batch(self, message, model="llama-3.1-70b-versatile", temperature=0):
        """
        Generates a response using the LLM in Batch mode.
        
        Parameters:
            message (str): The user input message/query.
            model (str): The model to use for generating the response.
            temperature (float): Controls the randomness of the response.
        
        Returns:
            response: The response object from the Groq API, or an error message.
        """
        try:
            # Request the LLM to generate a response in Batch mode (returns the whole response at once)
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": f"{self.sys_prompt}"},  # Add system prompt
                    {"role": "user", "content": message},                 # Add user query
                ],
                response_format={"type": "text"},  # Batch mode for full response
                temperature=temperature            # Temperature for response creativity
            )
            return response
                    
        except Exception as e:
            # Handle any errors that occur during the API call
            return {"error": str(e)}
