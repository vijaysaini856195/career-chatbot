import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json
import base64
import google.generativeai as genai

# --- Google Sheets Setup ---
try:
    # Decode the Base64 secret for Google Sheets
    creds_base64 = st.secrets["GCP_CREDENTIALS_BASE64"]
    creds_json_str = base64.b64decode(creds_base64).decode("utf-8")
    creds_dict = json.loads(creds_json_str)
    
    # Authenticate with Google Sheets
    creds = Credentials.from_service_account_info(creds_dict, scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ])
    client = gspread.authorize(creds)
    
    # Open the spreadsheet
    spreadsheet = client.open("New Career Chatbot Data")
    worksheet = spreadsheet.sheet1
except Exception as e:
    st.error(f"Error connecting to Google Sheets: {e}")
    st.stop()

# --- AI Model Setup ---
try:
    # Configure the generative AI model using the correct secret
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error configuring the AI model: {e}")
    st.stop()


# --- App Logic ---
st.title("🤖 AI Career Path Recommendation Chatbot by (vijay saini)")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if prompt := st.chat_input("What are your interests and skills?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- Get AI Response ---
    try:
        # Create a prompt for the AI
        ai_prompt = f"Based on these interests and skills: '{prompt}', recommend 3 potential career paths with a brief explanation for each."
        
        # Get the response from the model
        response = model.generate_content(ai_prompt)
        bot_response = response.text
    except Exception as e:
        bot_response = f"Sorry, I couldn't process that. Error: {e}"
    
    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)

    # --- Save to Google Sheets ---
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = [timestamp, prompt, bot_response]
        worksheet.append_row(new_row)
    except Exception as e:
        st.error(f"Failed to save data to Google Sheets: {e}")

