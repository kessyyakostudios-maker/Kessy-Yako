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
    
    /* Reset paddingu */
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        max-width: 100%;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }

    /* 2. FULL-SCREEN SEKCE */
    .section-container {
        min-height: 100vh;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 4rem 2rem;
    }

    /* HERO */
    .hero-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 5vw !important;
        color: #ffffff !important;
        letter-spacing: 2px;
        margin: 0;
        text-shadow: 0 10px 30px rgba(0,0,0,0.8);
        text-align: center;
    }
    
    .hero-subtitle {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 1.5rem !important;
        color: #888888 !important;
        letter-spacing: 5px;
        text-transform: uppercase;
        margin-top: 1rem;
        text-align: center;
    }

    /* NADPISY SEKCÍ */
    .section-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 3rem !important;
        color: #ffffff !important;
        margin-bottom: 3rem;
        text-align: center;
    }

    /* KARTY SLUŽEB (STEJNÁ VÝŠKA) */
    div[data-testid="column"] {
        background: rgba(255, 255, 255, 0.03);
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        height: 100%;
    }

    /* TLAČÍTKA */
    .stButton > button {
        background: #f0f0f0 !important;
        color: black !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 4px;
        padding: 0.8rem 2rem;
        width: 100%;
    }
    .stButton > button:hover {
        background: white !important;
        transform: scale(1.02);
    }

    /* INPUTY */
    .stTextArea textarea, .stTextInput input {
        background-color: #111 !important;
        color: white !important;
        border: 1px solid #333 !important;
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

# --- 1. HERO SEKCE (Start) ---
st.markdown("""
    <div class="section-container" style="background: radial-gradient(circle at center, #111 0%, #000 100%);">
        <h1 class="hero-title">Kessy Yako Studio</h1>
        <p class="hero-subtitle">Web Design</p>
        <div style="margin-top: 5rem; opacity: 0.5; font-size: 2rem;">↓</div>
    </div>
""", unsafe_allow_html=True)


# --- 2. AI KARIÉRNÍ NÁSTROJ (Full Screen) ---
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">AI Kariérní Nástroj</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    job = st.text_area("VLOŽTE INZERÁT", height=300, placeholder="Sem zkopírujte text inzerátu...")
with col2:
    cv = st.file_uploader("NAHRAJTE CV (PDF)", type="pdf")
    st.info("💡 Tip: AI vytvoří dopis na míru vašim zkušenostem.")

st.markdown("<br>", unsafe_allow_html=True)
if st.button("✨ VYGENEROVAT PROFESIONÁLNÍ DOPIS", use_container_width=True):
    if job and cv:
        with st.spinner("Analyzuji..."):
            try:
                txt = get_pdf_text(cv)
                model = genai.GenerativeModel('gemini-1.5-flash')
                res = model.generate_content(f"Napiš motivační dopis. Inzerát: {job}. CV: {txt}")
                st.markdown(f"<div style='background:#111; padding:30px; border:1px solid #333;'>{res.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Chyba: {e}")
st.markdown('</div>', unsafe_allow_html=True)


# --- 3. SLUŽBY (3 KARTY) ---
st.markdown('<div class="section-container" style="background: #080808;">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Co nabízíme</h2>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### 🎨 Webdesign & UI")
    st.write("Luxusní vizuální identita. Tvoříme weby, které budují důvěru a prodávají.")
    st.markdown("<br>", unsafe_allow_html=True)

with c2:
    st.markdown("### 💻 Development")
    st.write("Robustní systémy. E-shopy a aplikace na míru s důrazem na rychlost.")
    st.markdown("<br>", unsafe_allow_html=True)

with c3:
    st.markdown("### 🤖 AI Integrace")
    st.write("Automatizace procesů. Zapojte umělou inteligenci do vašeho podnikání.")
    st.markdown("<br>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# --- 4. KONTAKT ---
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Spolupráce</h2>', unsafe_allow_html=True)

contact_form = """
<form action="https://formspree.io/f/mpwvwwbj" method="POST" style="width: 100%; max-width: 600px; margin: 0 auto;">
    <input type="email" name="email" placeholder="Váš email" style="width: 100%; padding: 20px; margin-bottom: 15px; background: #111; border: 1px solid #333; color: white; border-radius: 5px;">
    <textarea name="message" rows="5" placeholder="Jak vám můžeme pomoci?" style="width: 100%; padding: 20px; margin-bottom: 25px; background: #111; border: 1px solid #333; color: white; border-radius: 5px;"></textarea>
    <button type="submit" style="width: 100%; padding: 20px; background: white; color: black; font-weight: bold; border: none; border-radius: 5px; cursor: pointer; font-size: 1.1rem;">ODESLAT POPTÁVKU</button>
</form>
"""
st.markdown(contact_form, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)