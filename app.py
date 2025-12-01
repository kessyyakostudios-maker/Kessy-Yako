import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# --- KONFIGURACE ---
st.set_page_config(page_title="Kessy Yako Studio", page_icon="✨", layout="wide", initial_sidebar_state="collapsed")

# --- CSS DESIGN ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap');

    /* 1. ZÁKLAD */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(at 50% 0%, #1a1a1a 0%, #000000 80%);
        color: #e0e0e0;
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Odstranění odsazení nahoře */
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        max-width: 100%;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }

    /* 2. HERO SEKCE (CELÁ OBRAZOVKA) */
    .hero-container {
        height: 100vh; /* 100% výšky okna */
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        background: radial-gradient(circle at center, #111 0%, #000 100%);
    }
    
    .hero-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 5vw !important; /* Velikost podle šířky obrazovky */
        color: #ffffff !important;
        letter-spacing: 2px;
        margin: 0;
        text-shadow: 0 10px 30px rgba(0,0,0,0.8);
    }
    
    .hero-subtitle {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 1.5rem !important;
        color: #888888 !important;
        letter-spacing: 5px;
        text-transform: uppercase;
        margin-top: 1rem;
    }

    /* Šipka dolů (animace) */
    .scroll-down {
        margin-top: 5rem;
        animation: bounce 2s infinite;
        opacity: 0.5;
        font-size: 2rem;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
        40% {transform: translateY(-10px);}
        60% {transform: translateY(-5px);}
    }

    /* 3. ZBYTEK WEBU (KONTEJNER) */
    .content-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 4rem 1rem;
    }

    /* TLAČÍTKA */
    .stButton > button {
        background: #f0f0f0 !important;
        color: black !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 4px;
        padding: 0.8rem 2rem;
    }
    .stButton > button:hover {
        background: white !important;
        transform: scale(1.05);
    }

    /* SKRYTÍ */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- LOGIKA ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    pass

def get_pdf_text(pdf_file):
    reader = PdfReader(pdf_file)
    return "".join([p.extract_text() for p in reader.pages])

# --- 1. HERO SEKCE (PŘES CELOU OBRAZOVKU) ---
st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">Kessy Yako Studio</h1>
        <p class="hero-subtitle">Web design</p>
        <div class="scroll-down">↓</div>
    </div>
""", unsafe_allow_html=True)


# --- 2. OBSAH WEBU (ZOBRAZÍ SE PO SCROLLOVÁNÍ) ---
# Vytvoříme kontejner, aby obsah nebyl nalepený na kraje
with st.container():
    st.markdown('<div class="content-container">', unsafe_allow_html=True)

    # A) AI GENERÁTOR
    st.markdown("<h2 style='text-align: center; font-family: Playfair Display; font-size: 2.5rem;'>AI Kariérní Nástroj</h2>", unsafe_allow_html=True)
    st.write("") 
    
    col1, col2 = st.columns([1,1])
    with col1:
        job = st.text_area("INZERÁT", height=150, placeholder="Vložte text inzerátu...")
    with col2:
        cv = st.file_uploader("CV (PDF)", type="pdf")
    
    if st.button("✨ VYGENEROVAT DOPIS", use_container_width=True):
        if job and cv:
            with st.spinner("Pracuji..."):
                try:
                    txt = get_pdf_text(cv)
                    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    model = genai.GenerativeModel(next((m for m in models if 'flash' in m), models[0]))
                    res = model.generate_content(f"Napiš motivační dopis. Inzerát: {job}. CV: {txt}")
                    st.markdown(f"<div style='background:#111; padding:20px; border:1px solid #333;'>{res.text}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Chyba: {e}")

    st.markdown("<br><br><hr style='border-color: #333;'><br>", unsafe_allow_html=True)

    # B) KONTAKT
    st.markdown("<h2 style='text-align: center; font-family: Playfair Display;'>Spolupráce</h2>", unsafe_allow_html=True)
    
    contact_form = """
    <form action="https://formspree.io/f/mpwvwwbj" method="POST">
        <input type="email" name="email" placeholder="Váš email" style="width: 100%; padding: 15px; margin-bottom: 10px; background: #0a0a0a; border: 1px solid #333; color: white;">
        <textarea name="message" rows="4" placeholder="Zpráva..." style="width: 100%; padding: 15px; margin-bottom: 20px; background: #0a0a0a; border: 1px solid #333; color: white;"></textarea>
        <button type="submit" style="width: 100%; padding: 15px; background: white; color: black; font-weight: bold; border: none; cursor: pointer;">ODESLAT</button>
    </form>
    """
    st.markdown(contact_form, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)