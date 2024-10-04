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

    # Priority Questions
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

    # Outfit Preferences
    top_preference = st.radio("What type of tops do you wear most often?", ["T-shirts", "Blouses", "Sweaters", "Hoodies"], index=0)
    bottom_preference = st.radio("What kind of bottoms do you prefer?", ["Jeans", "Trousers", "Skirts", "Shorts"], index=0)
    outerwear_preference = st.radio("What is your go-to outerwear?", ["Jacket", "Coat", "Blazer", "Sweater"], index=0)
    footwear_preference = st.radio("What’s your preferred footwear for daily wear?", ["Sneakers", "Boots", "Flats", "Heels"], index=0)
    dress_frequency = st.radio("How often do you wear dresses or jumpsuits?", ["Frequently", "Sometimes", "Rarely", "Never"], index=0)
    layering_preference = st.radio("Do you often layer your outfits?", ["Always", "Sometimes", "Rarely", "Never"], index=0)
    jeans_fit = st.radio("Which fit of jeans do you prefer?", ["Skinny", "Straight", "Bootcut", "Wide-leg"], index=0)
    formal_wear_frequency = st.radio("How often do you wear formal attire?", ["Daily", "Weekly", "Occasionally", "Rarely"], index=0)
    sportswear_preference = st.radio("What kind of sportswear do you prefer?", ["T-shirt and Shorts", "Tracksuit", "Leggings and Tank Top", "Compression Wear", "Sports Bra and Leggings", "Joggers and Hoodie"], index=0)
    party_outfit = st.radio("What do you usually wear to a party?", ["Dress", "Suit", "Casual", "Themed"], index=0)

    # Fashion Experience
    confidence_in_style = st.radio("Do you feel confident in your style choices?", ["Always", "Sometimes", "Rarely", "Never"], index=0)
    follow_fashion_trends = st.radio("Do you follow fashion trends?", ["Always", "Sometimes", "Rarely", "Never"], index=0)
    look_for_inspiration = st.radio("How often do you look for style inspiration?", ["Daily", "Weekly", "Occasionally", "Never"], index=0)
    wardrobe_satisfaction = st.radio("How do you feel about your wardrobe?", ["Satisfied", "Needs improvement", "Outdated", "Too small"], index=0)
    unique_style = st.radio("Would you describe your style as unique?", ["Yes", "No", "Unsure"], index=0)
    outfit_struggle = st.radio("How often do you struggle to find the right outfit?", ["Frequently", "Sometimes", "Rarely", "Never"], index=0)
    fashion_preference = st.radio("Do you prefer timeless fashion or fast fashion?", ["Timeless", "Fast fashion", "Mix of both"], index=0)
    gender_neutral_clothing = st.radio("Do you wear gender-neutral clothing?", ["Yes", "No", "Sometimes"], index=0)
    special_occasion_attire = st.radio("How often do you dress up for special occasions?", ["Frequently", "Sometimes", "Rarely", "Never"], index=0)
    trendsetter = st.radio("Would you consider yourself a trendsetter?", ["Yes", "No", "Unsure"], index=0)

    # Interaction with Fashion AI
    ai_usefulness = st.radio("How useful is the AI's fashion advice?", ["Very Useful", "Somewhat Useful", "Not Useful"], index=0)
    trust_in_ai = st.radio("Do you trust the AI's fashion suggestions?", ["Yes", "Sometimes", "No"], index=0)
    ai_preference = st.radio("Do you prefer more images or text-based recommendations?", ["Images", "Text", "Both"], index=0)
    ai_usage_frequency = st.radio("How often do you use the fashion AI?", ["Daily", "Weekly", "Occasionally", "Rarely"], index=0)
    ai_match_preferences = st.radio("Does the AI suggest products based on your preferences?", ["Always", "Sometimes", "Rarely", "Never"], index=0)
    ai_recommendation = st.radio("Would you recommend the fashion AI to others?", ["Yes", "No", "Maybe"], index=0)
    ai_understanding_style = st.radio("How would you rate the AI’s ability to understand your style?", ["Excellent", "Good", "Average", "Poor"], index=0)
    more_personalized_recommendations = st.radio("Would you like more personalized recommendations?", ["Yes", "No", "Maybe"], index=0)
    event_suggestions = st.radio("Is the AI helpful in suggesting outfits for events?", ["Yes", "No", "Sometimes"], index=0)
    ai_improvements = st.radio("What could the AI improve?", ["Better style understanding", "More personalized suggestions", "More trend advice", "Visual examples"], index=0)

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
            {"role": "user", "content": f"User input - Name: {name}, Age: {age}, Location: {location}, Gender: {gender}, Ethnicity: {ethnicity}, Height: {height}, Weight: {weight}, Skin Tone: {skin_tone}, Style Preference: {style_preference}, Color Palette: {color_palette}, Everyday Style: {everyday_style}, Preferred Prints: {preferred_prints}, Season: {season_preference}, Priority: {outfit_priority}, Experimenting: {experiment_with_trends}, Accessories: {accessories}, Fit: {fit_preference}, Material: {material_preference}, Top Preference: {top_preference}, Bottom Preference: {bottom_preference}, Outerwear Preference: {outerwear_preference}, Footwear Preference: {footwear_preference}, Dress Frequency: {dress_frequency}, Layering Preference: {layering_preference}, Jeans Fit: {jeans_fit}, Formal Wear Frequency: {formal_wear_frequency}, Sportswear Preference: {sportswear_preference}, Party Outfit: {party_outfit}, Confidence in Style: {confidence_in_style}, Follow Fashion Trends: {follow_fashion_trends}, Look for Inspiration: {look_for_inspiration}, Wardrobe Satisfaction: {wardrobe_satisfaction}, Unique Style: {unique_style}, Outfit Struggle: {outfit_struggle}, Fashion Preference: {fashion_preference}, Gender Neutral Clothing: {gender_neutral_clothing}, Special Occasion Attire: {special_occasion_attire}, Trendsetter: {trendsetter}, AI Usefulness: {ai_usefulness}, Trust in AI: {trust_in_ai}, AI Preference: {ai_preference}, AI Usage Frequency: {ai_usage_frequency}, AI Match Preferences: {ai_match_preferences}, AI Recommendation: {ai_recommendation}, AI Understanding Style: {ai_understanding_style}, More Personalized Recommendations: {more_personalized_recommendations}, Event Suggestions: {event_suggestions}, AI Improvements: {ai_improvements}"},
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
