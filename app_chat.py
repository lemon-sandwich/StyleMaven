import time
import os
import joblib
import streamlit as st
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.environ.get('GOOGLE_API_KEY')  # Make sure to set your API key in the .env file

# Set up the API endpoint and model
API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'
headers = {
    'Content-Type': 'application/json',
}

# Create a data/ folder if it doesn't already exist
try:
    os.mkdir('data/')
except:
    # data/ folder already exists
    pass

# Load past chats (if available)
try:
    past_chats: dict = joblib.load('data/past_chats_list')
except:
    past_chats = {}

# Sidebar for past chats
with st.sidebar:
    st.write('# Past Chats')
    st.session_state.chat_id = st.selectbox(
        label='Pick a past chat',
        options=list(past_chats.keys()) + ['New Chat'],
        format_func=lambda x: past_chats.get(x, 'New Chat'),
        placeholder='_',
    )
    st.session_state.chat_title = f'ChatSession-{st.session_state.chat_id}'

st.write('# Chat with Gemini')

# Chat history
try:
    st.session_state.messages = joblib.load(f'data/{st.session_state.chat_id}-st_messages')
except:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(name=message['role']):
        st.markdown(message['content'])

# Input fields for user data
age = st.number_input("Your Age", min_value=0)
gender = st.selectbox("Your Gender", ["Male", "Female", "Other"])
ethnicity = st.selectbox("Your Ethnicity", ["Asian", "Black", "Hispanic", "White", "Other"])

# React to user input
if prompt := st.chat_input('Your fashion query here...'):
    with st.chat_message('user'):
        st.markdown(prompt)

    # Prepare the input for the AI response
    context = f"Age: {age}, Gender: {gender}, Ethnicity: {ethnicity}. User question: {prompt}"
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": context
                    }
                ]
            }
        ]
    }

    try:
        # Send request to the Gemini API
        response = requests.post(API_URL, headers=headers, json=data, params={'key': API_KEY})
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the response
        response_data = response.json()
        ai_response = response_data.get('contents')[0]['parts'][0]['text']

        # Display assistant response
        with st.chat_message(name='ai'):
            st.markdown(ai_response)

        # Save chat history
        st.session_state.messages.append(dict(role='user', content=prompt))
        st.session_state.messages.append(dict(role='ai', content=ai_response))
        joblib.dump(st.session_state.messages, f'data/{st.session_state.chat_id}-st_messages')

    except Exception as e:
        with st.chat_message(name='ai'):
            st.markdown(f"An error occurred: {e}")
