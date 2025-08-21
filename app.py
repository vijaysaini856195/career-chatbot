# --- Google Sheets Setup ---
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

try:
    # Get credentials from Streamlit Secrets
    google_creds_dict = st.secrets["gcp_service_account"]

    creds = Credentials.from_service_account_info(google_creds_dict, scopes=[
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
