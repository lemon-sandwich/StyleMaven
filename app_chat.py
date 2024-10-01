import time
import os
import joblib
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = "AIzaSyA-ck6Z64xnAkr67pEMOFNNj9VEdpVRFA0"
genai.configure(api_key=GOOGLE_API_KEY)

# Chat session setup
new_chat_id = f'{time.time()}'
MODEL_ROLE = 'ai'
AI_AVATAR_ICON = '👗'

# Create a data/ folder if it doesn't already exist
try:
    os.mkdir('data/')
except FileExistsError:
    pass

# Load past chats (if available)
try:
    past_chats: dict = joblib.load('data/past_chats_list')
except FileNotFoundError:
    past_chats = {}

# Sidebar for past chats
with st.sidebar:
    st.write('# Past Chats')
    if st.session_state.get('chat_id') is None:
        st.session_state.chat_id = st.selectbox(
            label='Pick a past chat',
            options=[new_chat_id] + list(past_chats.keys()),
            format_func=lambda x: past_chats.get(x, 'New Chat'),
            placeholder='_',
        )
    else:
        st.session_state.chat_id = st.selectbox(
            label='Pick a past chat',
            options=[new_chat_id, st.session_state.chat_id] + list(past_chats.keys()),
            index=1,
            format_func=lambda x: past_chats.get(x, 'New Chat'),
            placeholder='_',
        )
    st.session_state.chat_title = f'ChatSession-{st.session_state.chat_id}'

# Main chat section
st.write('# Chat with Gemini Fashion Assistant')

# Load chat history
try:
    st.session_state.messages = joblib.load(f'data/{st.session_state.chat_id}-st_messages')
    st.session_state.gemini_history = joblib.load(f'data/{st.session_state.chat_id}-gemini_messages')
except FileNotFoundError:
    st.session_state.messages = []
    st.session_state.gemini_history = []

# Configure the model to use Gemini
st.session_state.model = genai.GenerativeModel('text-bison-001')  # Change to the desired model ID
st.session_state.chat = st.session_state.model.start_chat(
    history=st.session_state.gemini_history,
)

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(name=message['role'], avatar=message.get('avatar')):
        st.markdown(message['content'])

# Input fields for age, gender, and ethnicity
age = st.number_input("Enter your age:", min_value=0, max_value=120, value=25)
gender = st.selectbox("Select your gender:", options=["Male", "Female", "Non-binary", "Prefer not to say"])
ethnicity = st.selectbox("Select your ethnicity:", options=["Caucasian", "Hispanic", "African American", "Asian", "Other"])

# React to user text input
if prompt := st.chat_input('Your fashion query here...'):
    # Display user message
    with st.chat_message('user'):
        st.markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append(dict(role='user', content=prompt))

    # Prepare the input for the AI response
    context = f"Age: {age}, Gender: {gender}, Ethnicity: {ethnicity}. User question: {prompt}"
    
    # Send text input to the AI model
    response = st.session_state.chat.send_message(context, stream=True)

    # Display assistant response to text input
    with st.chat_message(name=MODEL_ROLE, avatar=AI_AVATAR_ICON):
        full_response = ''
        for chunk in response:
            for ch in chunk.text.split(' '):
                full_response += ch + ' '
                time.sleep(0.05)
            st.write(full_response)

    # Save chat history
    st.session_state.messages.append(dict(role=MODEL_ROLE, content=full_response, avatar=AI_AVATAR_ICON))
    st.session_state.gemini_history = st.session_state.chat.history
    joblib.dump(st.session_state.messages, f'data/{st.session_state.chat_id}-st_messages')
    joblib.dump(st.session_state.gemini_history, f'data/{st.session_state.chat_id}-gemini_messages')
