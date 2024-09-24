import streamlit as st
from PIL import Image
import pandas as pd
import openai
from dotenv import load_dotenv
import os
import PyPDF2
import io

load_dotenv()

# Initialize session state for memory
if 'case_memory' not in st.session_state:
    st.session_state.case_memory = ""

# Initialize session state for conversation history
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

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
    st.image("header.png", width=150) 
with col2:
    st.title("Dómagreining - Alpha útgáfa 1.0")
    st.caption("Þróunarverkefni")
    st.markdown("**Eftir Magnús Smára** | [www.smarason.is](https://www.smarason.is)")
    st.markdown("**Sækja API lykil:**")
    st.markdown("Til að nota þessa síðu þarft þú að sækja API lykil frá [OpenAI](https://platform.openai.com/api-keys).")
    st.markdown("Hver greining kostar nokkur cent þannig að þú þarft að virkja API áskrift til að nota þessa síðu.")
    st.write("Hlaðið upp PDF eða TXT skjali af íslenskum dómi og greinið með GPT-4")
    st.markdown("**Öll notkun á síðunni er undir MIT leyfi. Sjá nánari upplýsingar neðst á síðunni. Engum gögnum er safnað.**")
    st.markdown("Verkefnishlekkur og viðbótar upplýsingar: [https://github.com/Magnussmari/Domagreining/](https://github.com/Magnussmari/Domagreining/)")

# --- API Key Input ---
api_key = st.text_input("Sláðu inn OpenAI API lykilinn þinn:", type="password")
#api_key = os.getenv("OPENAI_API_KEY") þá getur þú keyrt þetta locally með því að setja OPENAI_API_KEY= í .env	

# --- File Uploader ---
uploaded_files = st.file_uploader("Veljið dómsskjal...", type=["pdf", "txt"], accept_multiple_files=True)

def extract_text_from_file(file):
    if file.type == "application/pdf":
        return extract_text_from_pdf(file)
    elif file.type == "text/plain":
        return file.getvalue().decode("utf-8")
    else:
        raise ValueError("Óþekkt skráarsnið")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def query_gpt_4(case_text, api_key):
    client = openai.OpenAI(api_key=api_key)
    prompt = f"""
    Greindu eftirfarandi íslenskan dóm og dragðu út lykilupplýsingar:

    {case_text}

    Vinsamlegast gefðu skipulagt vel uppsett svar með eftirfarandi köflum, hafðu það nægilega langt þannig að einstaklingur átti sig vel á lögfræðilegum álitamálum:
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

    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

def query_gpt_with_memory(case_text, follow_up, api_key):
    client = openai.OpenAI(api_key=api_key)
    
    messages = [
        {"role": "system", "content": f"You are an AI assistant analyzing the following Icelandic court case:\n\n{st.session_state.case_memory}"},
        {"role": "user", "content": follow_up}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=messages
    )

    return response.choices[0].message.content.strip()

if uploaded_files is not None:
    for uploaded_file in uploaded_files:
        try:
            case_text = extract_text_from_file(uploaded_file)

            # Show raw extracted text (for debugging)
            st.subheader("Útdreginn texti")
            st.text(case_text[:1000] + "...") # Show first 1000 characters

            # Step 1: Analyze the case
            if 'gpt_response' not in st.session_state:
                st.session_state.gpt_response = None

            if st.button("Greina mál"):
                with st.spinner("Greini málið..."):
                    st.session_state.gpt_response = query_gpt_4(case_text, api_key)
                    st.session_state.case_memory = case_text  # Store the case text in memory

            # Display the analysis if it exists
            if st.session_state.gpt_response:
                st.subheader("Greining málsins")
                st.markdown(st.session_state.gpt_response)

                # Add download button for full analysis
                original_filename = uploaded_file.name
                new_filename = os.path.splitext(original_filename)[0] + "_reifun.txt"
                st.download_button(
                    label="Hlaða niður fullri greiningu",
                    data=st.session_state.gpt_response,
                    file_name=new_filename,
                    mime="text/plain"
                )

            # Step 2: Follow-up Questions
            if st.session_state.case_memory:
                st.markdown("---")
                st.subheader("Spurðu út í dóminn")
                
                # Create a text input for questions
                follow_up = st.text_input("Settu inn spurningu þína hér:", key="follow_up")

                if st.button("Svara"):
                    if follow_up:
                        with st.spinner("Svarar..."):
                            follow_up_response = query_gpt_with_memory(st.session_state.case_memory, follow_up, api_key)
                        st.markdown("**Svar:**")
                        st.markdown(follow_up_response)
                        # Store the response in session state
                        st.session_state.last_response = follow_up_response
                    else:
                        st.warning("Vinsamlegast sláðu inn spurningu.")

                # Display the last response if it exists
                if 'last_response' in st.session_state:
                    st.markdown("**Síðasta svar:**")
                    st.markdown(st.session_state.last_response)

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