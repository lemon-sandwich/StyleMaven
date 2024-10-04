import streamlit as st 
from groq import Groq

# Initialize the Groq client with your API key
client = Groq(api_key="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")

# Define the system message for the model
system_message = {
    "role": "system",
    "content": "You are an experienced Fashion designer, taking inputs like name, age, gender, location, ethnicity, height, weight, skin tone, and style preferences to provide tailored fashion suggestions."
}

# Create a function to reset the chat
def reset_chat():
    st.session_state.messages = []
    st.session_state.chat_title = "New Chat"
    st.session_state.questionnaire_complete = False

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_title = "Fashion Assistant"
if 'questionnaire_complete' not in st.session_state:
    st.session_state.questionnaire_complete = False

# Sidebar for user inputs
with st.sidebar:
    st.header("User Inputs")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=100, value=25)
    location = st.text_input("Location")
    gender = st.selectbox("Gender", options=["Male", "Female", "Other"])
    ethnicity = st.selectbox("Ethnicity", options=["Asian", "Black", "Hispanic", "White", "Other"])
    height = st.number_input("Height (cm)", min_value=50, max_value=250, value=170)
    weight = st.number_input("Weight (kg)", min_value=20, max_value=200, value=70)
    skin_tone = st.text_input("Skin Tone (Hex Code)", value="#ffffff")

    if st.button("Reset Chat"):
        reset_chat()

# Display questionnaire if not completed
if not st.session_state.questionnaire_complete:
    st.header("Style Preferences Questionnaire")
    st.write("Please answer some questions if you don't mind. It's your choice to skip some if you like.")
    
    style_preference = st.radio("Which style do you prefer the most?", ["Casual", "Formal", "Streetwear", "Athleisure", "Baggy"], index=0)
    color_palette = st.radio("What color palette do you wear often?", ["Neutrals", "Bright Colors", "Pastels", "Dark Shades"], index=0)
    everyday_style = st.radio("How would you describe your everyday style?", ["Relaxed", "Trendy", "Elegant", "Bold"], index=0)
    preferred_prints = st.radio("What type of prints do you like?", ["Solid", "Stripes", "Floral", "Geometric", "Animal Print"], index=0)
    season_preference = st.radio("Which season influences your wardrobe the most?", ["Spring", "Summer", "Fall", "Winter"], index=0)
    outfit_priority = st.radio("What do you prioritize when choosing an outfit?", ["Comfort", "Style", "Affordability", "Brand"], index=0)
    experiment_with_trends = st.radio("How often do you experiment with new trends?", ["Always", "Sometimes", "Rarely", "Never"], index=0)
    accessories = st.radio("What kind of accessories do you usually wear?", ["Watches", "Rings", "Necklaces", "Bracelets", "Earrings"], index=0)
    fit_preference = st.radio("What fit do you prefer in clothes?", ["Loose", "Tailored", "Fitted", "Oversized"], index=0)
    material_preference = st.radio("Which material do you prefer?", ["Cotton", "Linen", "Silk", "Denim", "Wool"], index=0)

    if st.button("Submit Preferences"):
        st.session_state.questionnaire_complete = True
        st.success("Thank you! You can now start chatting.")
else:
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
            {"role": "user", "content": f"User input - Name: {name}, Age: {age}, Location: {location}, Gender: {gender}, Ethnicity: {ethnicity}, Height: {height}, Weight: {weight}, Skin Tone: {skin_tone}, Style Preference: {style_preference}, Color Palette: {color_palette}, Everyday Style: {everyday_style}, Preferred Prints: {preferred_prints}, Season: {season_preference}, Priority: {outfit_priority}, Experimenting: {experiment_with_trends}, Accessories: {accessories}, Fit: {fit_preference}, Material: {material_preference}"},
            {"role": "user", "content": user_input}
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
        with st.chat_message(name="assistant"):
            st.markdown(response_content)
