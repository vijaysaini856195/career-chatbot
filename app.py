# --- Google Sheets Setup ---
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json
import base64

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
