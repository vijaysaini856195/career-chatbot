import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# --- Google Sheets Setup ---
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds_file = "credentials.json" 

try:
    creds = Credentials.from_service_account_file(creds_file, scopes=scopes)
    client = gspread.authorize(creds)
    spreadsheet = client.open("New Career Chatbot Data")
    worksheet = spreadsheet.sheet1
except Exception as e:
    st.error(f"Error connecting to Google Sheets: {e}")
    st.stop()

# --- App Logic ---
st.title("🤖 Career Path Recommendation Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What are your interests?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    bot_response = f"You are interested in: {prompt}"
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)

    # --- Save to Google Sheets ---
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = [timestamp, prompt, bot_response]
        worksheet.append_row(new_row)
    except Exception as e:
        st.error(f"Failed to save data: {e}")