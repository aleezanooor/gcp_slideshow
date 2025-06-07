import streamlit as st
import gspread
import os
import json
import pandas as pd
import re
from datetime import datetime
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

# ────────────────────────────────────────
# Load Credentials from Env or .env
# ────────────────────────────────────────
load_dotenv()  # For local development

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

json_str = os.getenv("GCP_CREDENTIALS_JSON")
if not json_str:
    st.error("❌ Missing Google credentials. Please set GCP_CREDENTIALS_JSON.")
    st.stop()

try:
    creds_dict = json.loads(json_str)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
except Exception as e:
    st.error(f"❌ Failed to load credentials: {e}")
    st.stop()

# ────────────────────────────────────────
# Google Sheets Config
# ────────────────────────────────────────
SHEET_NAME = "SlideArchive"
WORKSHEET = "Slides"

@st.cache_resource
def get_gsheet():
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).worksheet(WORKSHEET)

def append_slide_entry(date, title, url):
    sheet = get_gsheet()
    sheet.append_row([str(date), title.strip(), url.strip()])

def fetch_slide_entries():
    sheet = get_gsheet()
    records = sheet.get_all_records()
    return pd.DataFrame(records)

# ────────────────────────────────────────
# Page Setup & Header
# ────────────────────────────────────────
st.set_page_config(page_title="Slide Deck Archive", layout="wide")

st.markdown("""
    <div style="background: linear-gradient(to right, #6a4c93, #8e5bd3);
                padding: 1.2rem; border-radius: 12px; margin-bottom: 2rem;
                color: white; font-family: 'Segoe UI', sans-serif;">
        <h2 style='margin-bottom: 0;'>📊 Slide Deck Archive Dashboard</h2>
        <p style='margin-top: 0.2rem; font-size: 0.9rem;'>Upload, manage, and view Google Slide decks centrally</p>
    </div>
""", unsafe_allow_html=True)

# ────────────────────────────────────────
# Upload Section
# ────────────────────────────────────────
with st.container():
    st.subheader("📤 Upload a New Slide Deck")

    st.markdown("""
    Use the form below to add a new presentation to the archive.  
    <span style='font-size: 0.85rem;'>
    📎 <a href="/Instructions" target="_self" style='color: #c3a8fa; text-decoration: none;'>
    How to get your Google Slides embed link</a>
    </span>
    """, unsafe_allow_html=True)

    with st.form("upload_form", border=True):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("📅 Presentation Date", value=datetime.today())
        with col2:
            title = st.text_input("📝 Title of Presentation")

        embed_input = st.text_area("🔗 Google Slides Embed Code or Direct URL")
        submitted = st.form_submit_button("Add to Archive", use_container_width=True)

        if submitted:
            match = re.search(r'src="([^"]+)"', embed_input)
            cleaned_url = match.group(1) if match else embed_input.strip()

            if not cleaned_url.startswith("https://docs.google.com/presentation/"):
                st.warning("❌ Invalid embed URL. Please use a valid Google Slides link.")
            else:
                append_slide_entry(date, title, cleaned_url)
                st.success("✅ Slide deck added to archive!")

st.divider()

# ────────────────────────────────────────
# Archive Viewer
# ────────────────────────────────────────
st.subheader("📚 View Slide Decks")

df = fetch_slide_entries()

if df.empty:
    st.info("No slide decks available yet. Add one above to get started.")
else:
    df["Label"] = df["Date"] + ": " + df["Title"]

    with st.container():
        col1, col2 = st.columns([2, 5])
        with col1:
            selected_label = st.selectbox("Select a deck to view:", df["Label"].tolist())
        with col2:
            selected_url = df.loc[df["Label"] == selected_label, "Embed URL"].values[0]
            st.markdown("#### 👇 Preview")
            st.markdown(
                f"""
                <iframe src="{selected_url}" frameborder="0"
                        width="100%" height="480px"
                        allowfullscreen></iframe>
                """,
                unsafe_allow_html=True
            )

# ────────────────────────────────────────
# Footer
# ────────────────────────────────────────
st.markdown("""
<hr style="margin-top: 2rem;"/>
<p style="font-size: 0.85rem; text-align: center;">
    Need help? Contact <strong>Aleeza Noor</strong> at 
    <a href="mailto:aleeza.noor@publicissapient.com">aleeza.noor@publicissapient.com</a>
</p>
""", unsafe_allow_html=True)
