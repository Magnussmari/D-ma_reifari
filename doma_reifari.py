import streamlit as st
from PIL import Image
import pandas as pd
import openai
from dotenv import load_dotenv
import os
import PyPDF2
import io

load_dotenv()

# --- Styling ---
st.markdown(
    """
    <style>
    .reportview-container {
        background-color: #f5f5f5;
    }
    .sidebar .sidebar-content {
        background-color: #e0e0e0;
    }
    h1 {
        color: #336699;
        font-family: 'Arial', sans-serif;
    }
    h2, h3 {
        color: #4d4d4d;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #336699;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px; 
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Header ---
col1, col2 = st.columns([1, 3])
with col1:
    # Placeholder for your logo (replace with actual image URL later)
    st.image("header.png", width=200) 
with col2:
    st.title("Dómagreining")
    st.markdown("**Eftir Magnús Smára** | [www.smarason.is](https://www.smarason.is)")
    st.write("Hlaðið upp PDF eða TXT skjali af íslenskum dómi og greinið þær með GPT-4o")

# --- API Key Input ---
api_key = st.text_input("Sláðu inn OpenAI API lykilinn þinn:", type="password")
#api_key = os.getenv("OPENAI_API_KEY") þá getur þú keyrt þetta locally með því að setja OPENAI_API_KEY= í .env	

# --- File Uploader ---
uploaded_file = st.file_uploader("Veljið dómsskjal...", type=["pdf", "txt"])

def extract_text_from_file(file):
    if file.type == "application/pdf":
        return extract_text_from_pdf(file)
    elif file.type == "text/plain":
        return file.getvalue().decode("utf-8")
    else:
        raise ValueError("Óstuddur skráarsnið")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def query_gpt_4(case_text, api_key):
    openai.api_key = api_key
    prompt = f"""
    Greindu eftirfarandi íslenskan dóm og dragðu út lykilupplýsingar:

    {case_text}

    Vinsamlegast gefðu skipulagða svörun með eftirfarandi köflum:
    Titill: Dómstóll - Númer málsins
    1. Samantekt málsins
    2. Lykilstaðreyndir
    3. Lagaleg rök
    4. Tilvísanir í lög og reglugerðir
    5. Tilvísanir í aðra dóma
    6. Tilvísanir í aðrar réttarheimildir
    7. Úrskurður dómstólsins
    8. Áhrif á lögfræðilega rannsókn

    Fyrir hvern kafla, veittu hnitmiðaðar og viðeigandi upplýsingar dregnar út úr texta málsins.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message['content'].strip()

if uploaded_file is not None and api_key:
    # Extract text from the uploaded file
    try:
        case_text = extract_text_from_file(uploaded_file)

        # Show raw extracted text (for debugging)
        st.subheader("Útdreginn texti")
        st.text(case_text[:1000] + "...") # Show first 1000 characters

        # Button to analyze the case with GPT-4
        if st.button("Greina mál"):
            with st.spinner("Greini málið..."):
                gpt_response = query_gpt_4(case_text, api_key)
            st.subheader("Greining málsins")
            st.markdown(gpt_response)

        # Add download button for full analysis
        if 'gpt_response' in locals():
            original_filename = uploaded_file.name
            new_filename = os.path.splitext(original_filename)[0] + "_reifun.txt"
            st.download_button(
                label="Hlaða niður fullri greiningu",
                data=gpt_response,
                file_name=new_filename,
                mime="text/plain"
            )
    except ValueError as e:
        st.error(f"Villa: {str(e)}")

# --- Footer ---
st.markdown(
    """
    <hr>
    <p style='text-align: center;'>
    Notkun er alfarið á eigin ábyrgð! Magnús Smári 2024. 
    <a href="https://opensource.org/licenses/MIT" target="_blank">MIT leyfi</a>
    </p>
    """,
    unsafe_allow_html=True,
)