import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# --- KONFIGURACE ---
st.set_page_config(page_title="Kessy Yako Studio", page_icon="✨", layout="wide", initial_sidebar_state="collapsed")

# --- CSS DESIGN (LUXUSNÍ FULL-HEIGHT) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap');

    /* 1. ZÁKLAD STRÁNKY */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(at 50% 0%, #1a1a1a 0%, #000000 80%);
        color: #e0e0e0;
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Odstranění horního odsazení Streamlitu, aby to bylo až ke stropu */
    .main .block-container {
        padding-top: 1rem !important;
        max-width: 1200px;
    }

    /* 2. HERO SEKCE PŘES CELOU OBRAZOVKU */
    .hero-container {
        min-height: 90vh; /* 90% výšky obrazovky */
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding-bottom: 5rem; /* Místo pro scrollování dolů */
    }
    
    .hero-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 6rem !important;
        font-weight: 700;
        color: #ffffff !important;
        letter-spacing: 4px;
        margin-bottom: 1rem;
        text-shadow: 0 4px 15px rgba(0,0,0,0.8);
    }
    
    .hero-subtitle {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 1.5rem !important;
        font-weight: 300;
        color: #cccccc !important;
        letter-spacing: 6px;
        text-transform: uppercase;
    }

    /* 3. TYPOGRAFIE ZBYTKU STRÁNKY */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #ffffff !important;
    }

    /* 4. OPRAVA TLAČÍTEK (ABY BYLA ČITELNÁ) */
    .stButton > button {
        background: #f0f0f0 !important;
        color: #000000 !important; /* NATVRDO ČERNÁ BARVA */
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        border-radius: 4px !important;
        border: none !important;
        padding: 1rem 2rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton > button:hover {
        background: #ffffff !important;
        box-shadow: 0 0 15px rgba(255,255,255,0.3) !important;
        transform: scale(1.02);
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

# --- OBSAH WEBU ---

# 1. HERO SEKCE (PŘES CELOU OBRAZOVKU)
# Toto je ten HTML blok, který zajistí výšku
st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">KESSY YAKO</h1>
        <p class="hero-subtitle">DIGITAL STUDIO & AI LAB</p>
    </div>
""", unsafe_allow_html=True)


# --- ZBYTEK STRÁNKY (UKÁŽE SE AŽ PO SCROLLOVÁNÍ) ---

st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

# 2. AI NÁSTROJ
st.markdown("<h2 style='text-align: center;'>Nástroje budoucnosti</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-bottom: 3rem;'>Vyzkoušejte sílu AI na vlastní kůži.</p>", unsafe_allow_html=True)

col_in1, col_in2 = st.columns([1, 1])
with col_in1:
    job = st.text_area("TEXT INZERÁTU", height=200, placeholder="Vložte text nabídky práce...")
with col_in2:
    cv = st.file_uploader("VAŠE CV (PDF)", type="pdf")

if st.button("✨ VYGENEROVAT MOTIVAČNÍ DOPIS", use_container_width=True):
    if job and cv:
        with st.spinner("Generuji..."):
            try:
                txt = get_pdf_text(cv)
                models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                model = genai.GenerativeModel(next((m for m in models if 'flash' in m), models[0]))
                res = model.generate_content(f"Napiš motivační dopis česky. Inzerát: {job}. CV: {txt}")
                st.markdown(f"<div style='background:#111; padding:30px; border-radius:10px; margin-top:20px; border: 1px solid #333;'>{res.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Chyba: {e}")

st.markdown("<br><br><hr><br>", unsafe_allow_html=True)

# 3. SLUŽBY
st.markdown("<h2 style='text-align: center; margin-bottom: 3rem;'>Naše služby</h2>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("### Webdesign & UI")
    st.write("Luxusní vizuální identita, která prodává.")
with c2:
    st.markdown("### Development")
    st.write("Robustní systémy a e-shopy na míru.")
with c3:
    st.markdown("### AI Integrace")
    st.write("Automatizace firemních procesů.")

st.markdown("<br><br><hr><br>", unsafe_allow_html=True)

# 4. KONTAKT
st.markdown("<h2 style='text-align: center;'>Kontaktujte nás</h2>", unsafe_allow_html=True)
contact_form = """
<form action="https://formspree.io/f/mpwvwwbj" method="POST" style="max-width: 600px; margin: 0 auto;">
    <input type="email" name="email" placeholder="Váš email" style="width: 100%; padding: 15px; margin-bottom: 10px; background: #0a0a0a; border: 1px solid #333; color: white;">
    <textarea name="message" rows="4" placeholder="Zpráva..." style="width: 100%; padding: 15px; margin-bottom: 20px; background: #0a0a0a; border: 1px solid #333; color: white;"></textarea>
    <button type="submit" style="width: 100%; padding: 15px; background: white; color: black; font-weight: bold; border: none; cursor: pointer;">ODESLAT</button>
</form>
"""
st.markdown(contact_form, unsafe_allow_html=True)
st.markdown("<br><br><h1 style='text-align: center; opacity: 0.2; font-size: 2rem;'>KY</h1>", unsafe_allow_html=True)