import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json
import base64
import google.generativeai as genai
from googleapiclient.discovery import build

# --- Setup Section ---

# Function to search for a YouTube video
def youtube_search(query):
    try:
        # NOTE: You would need a YouTube Data API key for this to work reliably.
        # For now, this is a placeholder showing how it would be structured.
        # A simple Google search can be an alternative if the API is not available.
        # This function will simulate a search result for demonstration.
        search_query = f"{query} career path explanation youtube"
        # In a real app, you'd use the YouTube API here.
        # For example:
        # youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        # request = youtube.search().list(q=search_query, part='snippet', type='video', maxResults=1)
        # response = request.execute()
        # video_id = response['items'][0]['id']['videoId']
        # video_title = response['items'][0]['snippet']['title']
        # video_url = f"https://www.youtube.com/watch?v={video_id}"
        # return video_title, video_url
        
        # Simulated search result for now
        # To make this real, you'd need to set up a YouTube Data API key and add it to secrets
        return "A Guide to the Career Path", "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # Placeholder link
    except Exception as e:
        print(f"YouTube search failed: {e}")
        return None, None

# --- Google Sheets Setup ---
try:
    creds_base64 = st.secrets["GCP_CREDENTIALS_BASE64"]
    creds_json_str = base64.b64decode(creds_base64).decode("utf-8")
    creds_dict = json.loads(creds_json_str)
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

# --- AI Model Setup ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error configuring the AI model: {e}")
    st.stop()


# --- App Logic ---
st.title("🤖 AI Career Path Recommendation Chatbot by vijay")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What are your interests and skills?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- Get AI or Greeting Response ---
    try:
        greetings = ["hello", "hi", "hey", "hii", "helo"]
        if prompt.lower().strip() in greetings:
            bot_response = "Hello! How can I help you with your career path today? Ask me about any field."
        else:
            # 1. Improved AI Prompt
            ai_prompt = f"""
            You are an expert Career Counselor named 'Career Bot by Vijay'. 
            Your goal is to provide detailed, helpful, and encouraging career advice.
            A user is interested in: '{prompt}'.

            Please provide a response that includes:
            1. A brief, encouraging introduction to the field.
            2. At least 3 Pros (benefits) of a career in this field.
            3. At least 3 Cons (challenges) of a career in this field.
            4. A short "Getting Started" guide with 2-3 actionable steps.
            5. Keep the tone professional yet friendly.
            """
            
            # 2. Get the AI's detailed text response
            response = model.generate_content(ai_prompt)
            bot_response_text = response.text

            # 3. Search for a relevant YouTube video
            video_title, video_url = youtube_search(prompt)
            
            # 4. Combine the text and video link into the final response
            if video_url:
                bot_response = f"{bot_response_text}\n\n---\n\n🎥 **Here is a helpful video to get you started:**\n\n[{video_title}]({video_url})"
            else:
                bot_response = bot_response_text

    except Exception as e:
        bot_response = f"Sorry, I couldn't process that. Error: {e}"
    
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response, unsafe_allow_html=True)

    # --- Save to Google Sheets ---
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = [timestamp, prompt, bot_response]
        worksheet.append_row(new_row)
    except Exception as e:
        st.error(f"Failed to save data to Google Sheets: {e}")
