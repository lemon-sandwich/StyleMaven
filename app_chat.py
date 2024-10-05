import streamlit as st
from groq import Groq
from PIL import Image

# Initialize the Groq client with your API key
client = Groq(api_key="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")

# Define the system message for the model
system_message = {
    "role": "system",
    "content": "You are an experienced fashion designer who provides fashion compliments based on images. Compliment the user's outfit, colors, and overall fashion sense. Stay friendly and positive."
}

# Function to reset the chat
def reset_chat():
    st.session_state.messages = []
    st.session_state.chat_title = "Fashion Assistant"

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_title = "Fashion Assistant"

# Sidebar for image upload
with st.sidebar:
    st.header("Upload Your Image")
    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if st.button("Reset Chat"):
        reset_chat()

# Display the uploaded image
if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Your uploaded image", use_column_width=True)

    # Store user message in the chat history for displaying the image
    st.session_state.messages.append({"role": "user", "content": "User uploaded an image."})

    # Prepare messages for the API call
    messages = [
        system_message,
        {"role": "user", "content": "The user has uploaded an image. Please give a compliment based on the outfit and style in the image."}
    ]

    try:
        # Generate a response from the Groq API
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
        )

        # Ensure response is valid
        if completion.choices and len(completion.choices) > 0:
            response_content = completion.choices[0].message.content
        else:
            response_content = "Sorry, I couldn't generate a response."

    except Exception as e:
        response_content = f"Error: {str(e)}"

    # Store assistant response in the chat history
    st.session_state.messages.append({"role": "assistant", "content": response_content})

    # Display assistant response
    st.markdown(f"**Fashion Assistant:** {response_content}")
else:
    st.write("Please upload an image to get fashion advice.")

# Display all previous chat messages
st.title(st.session_state.chat_title)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
