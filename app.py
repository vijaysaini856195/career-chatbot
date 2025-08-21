# --- Google Sheets Setup ---
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json

try:
    # Load the credentials from the single secret
    creds_json_str = st.secrets["GOOGLE_CREDENTIALS_JSON"]
    creds_dict = json.loads(creds_json_str) # Convert the string to a dictionary
    
    creds = Credentials.from_service_account_info(creds_dict, scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ])
    client = gspread.authorize(creds)
    
    spreadsheet = client.open("New Career Chatbot Data")
    worksheet = spreadsheet.sheet1
except Exception as e:
    st.error(f"Error connecting to Google Sheets: {e}")
    st.stop()
