import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json
import base64

# --- Google Sheets Setup ---
try:
    # Decode the Base64 secret and load it as a dictionary
    creds_base64 = st.secrets["GCP_CREDENTIALS_BASE64"]
    creds_json_str = base64.b64decode(creds_base64).decode("utf-8")
    creds_dict = json.loads(creds_json_str)
    
    # Authenticate with Google Sheets
    creds = Credentials.from_service_account_info(creds_dict, scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ])
    client = gspread.authorize(creds)
    
    # Make sure this name matches your Google Sheet name exactly
    spreadsheet = client.open("New Career Chatbot Data")
    worksheet = spreadsheet.sheet1
except Exception as e:
    st.error(f"Error connecting to Google Sheets: {e}")
    st.stop()

# --- App Logic ---
st.title("🤖 Career Path Recommendation Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if prompt := st.chat_input("What are your interests?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Define a simple bot response
    bot_response = f"You are interested in: {prompt}"
    
    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)

    # --- Save to Google Sheets ---
    try:
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create a new row with the data
        new_row = [timestamp, prompt, bot_response]
        
        # Append the new row to the worksheet
        worksheet.append_row(new_row)
    except Exception as e:
        st.error(f"Failed to save data to Google Sheets: {e}")
