pip install --upgrade openai

import os
import openai
import streamlit as st

# Configure OpenAI API key
openai.api_key = "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"

# Initialize Streamlit app
st.title("Fashion Assistant Chatbot")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Inputs for user details
age = st.number_input("Age", min_value=1, max_value=120)
gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"])
ethnicity = st.text_input("Ethnicity")

# User input for the chatbot
user_input = st.text_input("Your fashion-related question:")

# Function to reset chat
def reset_chat():
    st.session_state.messages = []

# Button to reset chat
if st.button("Reset Chat"):
    reset_chat()

# Display chat history
if st.session_state.messages:
    for msg in st.session_state.messages:
        st.markdown(f"**{msg['role']}**: {msg['content']}")

# Process user input
if st.button("Ask"):
    if user_input and gender != "Select" and ethnicity:
        context = f"You are a fashion assistant. User details: Age: {age}, Gender: {gender}, Ethnicity: {ethnicity}. User question: {user_input}"
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Call OpenAI API for response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Change to the desired model
            messages=[
                {"role": "system", "content": "You are a fashion assistant."},
                {"role": "user", "content": context}
            ]
        )

        assistant_message = response['choices'][0]['message']['content']
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})

        # Display assistant response
        st.markdown(f"**Assistant**: {assistant_message}")
    else:
        st.error("Please fill in all fields before asking.")
