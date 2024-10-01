import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Streamlit app layout
st.title("Tailored Fashion Assistant")

# User input fields
age = st.number_input("Enter your age:", min_value=0, max_value=100, value=23)
gender = st.selectbox("Select your gender:", ["Male", "Female", "Other"])
ethnicity = st.text_input("Enter your ethnicity (optional):")

# Ask for user query
user_query = st.text_input("What would you like to know about fashion?")

# Generate fashion suggestions based on user input
if st.button("Get Fashion Suggestions"):
    # Prepare the input for the model
    user_input = f"Input: Age: {age}, Gender: {gender}, Ethnicity: {ethnicity}, Question: {user_query}"
    
    # Generate content using the model
    response = model.generate_content([
        user_input,
        "Output: "
    ])

    # Display the model's response
    st.write("### Suggestions:")
    st.write(response.text)
