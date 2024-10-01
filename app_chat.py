import streamlit as st
from groq import Groq

# Initialize the Groq client with your API key
client = Groq(api_key="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")

# Define the system message for the model
system_message = {
    "role": "system",
    "content": "You are an experienced Fashion designer, taking inputs like gender, age, and ethnicity to provide tailored fashion suggestions."
}

# Create a function to reset the chat
def reset_chat():
    st.session_state.messages = []
    st.session_state.chat_title = "New Chat"

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_title = "Fashion Assistant"

# Sidebar for user inputs
with st.sidebar:
    st.header("User Inputs")
    age = st.number_input("Age", min_value=1, max_value=100, value=25)
    gender = st.selectbox("Gender", options=["Male", "Female", "Other"])
    ethnicity = st.selectbox("Ethnicity", options=["Asian", "Black", "Hispanic", "White", "Other"])
    if st.button("Reset Chat"):
        reset_chat()

# Display chat title
st.write(f"# {st.session_state.chat_title}")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(name=message['role']):
        st.markdown(message['content'])

# Handle user input
if user_input := st.chat_input("Ask me anything about fashion..."):
    # Store user message in the chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare messages for the API call
    messages = [
        system_message,
        {"role": "user", "content": f"User input - Age: {age}, Gender: {gender}, Ethnicity: {ethnicity}"},
        {"role": "user", "content": user_input}
    ]

    # Generate a response from the Groq API
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
    )

    response_content = completion.choices[0].message.content

    # Store assistant response in the chat history
    st.session_state.messages.append({"role": "assistant", "content": response_content})

    # Display assistant response
    with st.chat_message(name="assistant"):
        st.markdown(response_content)
