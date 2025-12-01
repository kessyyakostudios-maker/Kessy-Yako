import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# --- KONFIGURACE ---
st.set_page_config(page_title="Kessy Yako Studio", page_icon="✨", layout="wide", initial_sidebar_state="collapsed")

# --- CSS DESIGN (FINÁLNÍ FIX) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&display=swap');

    /* 1. ZÁKLAD STRÁNKY A POZADÍ */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(at 50% 0%, #1a1a1a 0%, #000000 80%);
        color: #e0e0e0;
        font-family: 'Montserrat', sans-serif;
    }
    
    /* 2. ODSTRANĚNÍ SVĚTLÉ LIŠTY NAHOŘE (KLÍČOVÉ) */
    header {
        visibility: hidden !important;
        background-color: transparent !important;
    }
    div[data-testid="stDecoration"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Posunutí obsahu úplně nahoru */
    .main .block-container {
        padding-top: 0 !important;
        max-width: 100%;
    }

    /* 3. HERO SEKCE */
    .hero-container {
        height: 100vh;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        background: transparent; /* Průhledné, aby byl vidět gradient stApp */
    }
    
    .hero-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 5vw !important;
        font-weight: 700;
        color: #ffffff !important;
        letter-spacing: 2px;
        margin: 0;
        text-shadow: 0 10px 30px rgba(0,0,0,0.8);
    }
    
    .hero-subtitle {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 1.5rem !important;
        font-weight: 400;
        color: #888888 !important;
        letter-spacing: 8px;
        text-transform: uppercase;
        margin-top: 1rem;
    }

    /* Šipka dolů */
    .scroll-down {
        margin-top: 6rem;
        animation: bounce 2s infinite;
        opacity: 0.5;
        font-size: 2rem;
        color: white;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
        40% {transform: translateY(-10px);}
        60% {transform: translateY(-5px);}
    }

    /* 4. TLAČÍTKA (Sytě černý text) */
    .stButton > button {
        background: #e0e0e0 !important; /* Stříbrná */
        color: #000000 !important;      /* ČERNÁ */
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 900 !important;    /* EXTRA TUČNÉ */
        border: none !important;
        border-radius: 4px;
        padding: 1rem 2rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .stButton > button:hover {
        background: #ffffff !important;
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(255,255,255,0.4);
    }
    
    /* Styl pro tlačítka v dialogu */
    div[role="dialog"] button {
        color: black !important;
        font-weight: bold !important;
    }

    /* 5. VYSKAKOVACÍ OKNA (MODALS) - Tmavé */
    div[data-testid="stDialog"] {
        background-color: #111111 !important;
        border: 1px solid #333;
        color: white !important;
    }

    /* 6. INPUTY */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #0a0a0a !important;
        color: white !important;
        border: 1px solid #333 !important;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #ffffff !important;
    }

    /* Skrytí patičky */
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
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
        <p class="hero-subtitle">Web Design</p>
        <div class="scroll-down">↓</div>
    </div>
""", unsafe_allow_html=True)


# --- 2. OBSAH WEBU (ZOBRAZÍ SE PO SCROLLOVÁNÍ) ---
with st.container():
    # Odsazení, aby obsah nebyl hned pod herem
    st.markdown('<div style="padding-top: 5rem;"></div>', unsafe_allow_html=True)

    # A) AI GENERÁTOR
    st.markdown("<h2 style='text-align: center; font-family: Playfair Display; font-size: 2.5rem; margin-bottom: 2rem;'>AI Kariérní Nástroj</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1,1])
    with col1:
        job = st.text_area("INZERÁT", height=150, placeholder="Vložte text inzerátu...")
    with col2:
        cv = st.file_uploader("CV (PDF)", type="pdf")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tlačítko na střed
    c_spacel, c_btn, c_spacer = st.columns([1,2,1])
    with c_btn:
        if st.button("✨ VYGENEROVAT DOPIS", use_container_width=True):
            if job and cv:
                with st.spinner("Pracuji..."):
                    try:
                        txt = get_pdf_text(cv)
                        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                        model = genai.GenerativeModel(next((m for m in models if 'flash' in m), models[0]))
                        res = model.generate_content(f"Napiš motivační dopis. Inzerát: {job}. CV: {txt}")
                        st.markdown(f"<div style='background:#111; padding:20px; border:1px solid #333; margin-top: 20px;'>{res.text}</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Chyba: {e}")

    st.markdown("<br><br><hr style='border-color: #333;'><br>", unsafe_allow_html=True)

    # B) KONTAKT
    st.markdown("<h2 style='text-align: center; font-family: Playfair Display; font-size: 2.5rem; margin-bottom: 2rem;'>Spolupráce</h2>", unsafe_allow_html=True)
    
    contact_form = """
    <form action="https://formspree.io/f/mpwvwwbj" method="POST" style="max-width: 700px; margin: 0 auto;">
        <input type="email" name="email" placeholder="Váš email" style="width: 100%; padding: 15px; margin-bottom: 15px; background: #0a0a0a; border: 1px solid #333; color: white; font-family: sans-serif;">
        <textarea name="message" rows="5" placeholder="Zpráva..." style="width: 100%; padding: 15px; margin-bottom: 25px; background: #0a0a0a; border: 1px solid #333; color: white; font-family: sans-serif;"></textarea>
        <button type="submit" style="width: 100%; padding: 15px; background: #e0e0e0; color: black; font-weight: 900; border: none; cursor: pointer; text-transform: uppercase; letter-spacing: 1px;">ODESLAT</button>
    </form>
    """
    st.markdown(contact_form, unsafe_allow_html=True)
    
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)