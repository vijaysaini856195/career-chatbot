# --- Google Sheets Setup ---
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json
import base64

try:
    # Decode the Base64 secret
    creds_base64 = st.secrets["GCP_CREDENTIALS_BASE64"]
    creds_json_str = base64.b64decode(creds_base64).decode("utf-8")
    creds_dict = json.loads(creds_json_str)
    # ... rest of the code
