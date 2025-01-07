import google.generativeai as genai
import os
from datetime import datetime

# Configure the Gemini API
GOOGLE_API_KEY = 'AIzaSyCR1XaDcTAYZ3_Em_WVOkUt5LnYuXJTVtk'

try:
    # Initialize the API
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # Create the model instance
    model = genai.GenerativeModel('gemini-pro')
    
    # Test the connection
    print("Testing API connection...")
    test_response = model.generate_content("Hello, testing connection.")
    if test_response.text:
        print("API connection successful!")
    else:
        print("API connection test failed - no response text")
        
except Exception as e:
    print(f"Error initializing API: {str(e)}")

def get_response(message):
    try:
        # Simple prompt structure
        prompt = f"""
        You are a travel assistant for JointJourneys travel agency.
        User question: {message}
        Please provide a helpful response:
        """
        
        # Log the attempt
        print(f"Attempting to get response for: {message}")
        
        # Generate response
        response = model.generate_content(prompt)
        
        # Check response
        if hasattr(response, 'text') and response.text:
            return response.text.strip()
        else:
            print("No response text received")
            return "I apologize, I couldn't generate a response. Please try again."
            
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return "I'm having trouble connecting to the service. Please try again later."

def is_api_working():
    try:
        test_response = model.generate_content("Test")
        return bool(test_response.text)
    except:
        return False 