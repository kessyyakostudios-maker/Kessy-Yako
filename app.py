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
    
    /* 2. SKRYTÍ LIŠTY (OPRAVENO) */
    header {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    div[data-testid="stDecoration"] {display: none !important;}
    
    /* Reset paddingu */
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        max-width: 100%;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }

    /* 3. HERO SEKCE (CELÁ OBRAZOVKA) */
    .hero-container {
        height: 100vh;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        background: transparent;
    }
    
    .hero-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 5vw !important;
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

    /* Šipka dolů */
    .scroll-down {
        margin-top: 5rem;
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

    /* 4. KONTEJNER PRO OBSAH */
    .content-container {
        max-width: 1100px;
        margin: 0 auto;
        padding: 6rem 2rem;
    }

    /* 5. TLAČÍTKA (ČERNÉ PÍSMO!) */
    .stButton > button {
        background: #f0f0f0 !important;
        color: #000000 !important; /* ČERNÁ */
        font-weight: 800 !important; /* TUČNÉ */
        border: none !important;
        border-radius: 4px;
        padding: 1rem 2rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton > button:hover {
        background: white !important;
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(255,255,255,0.2);
    }
    
    /* INPUTY */
    .stTextArea textarea, .stTextInput input {
        background-color: #111 !important;
        color: white !important;
        border: 1px solid #333 !important;
    }
    
    /* Nadpisy sekcí */
    h2 {
        font-family: 'Playfair Display', serif !important;
        font-size: 3rem !important;
        text-align: center;
        margin-bottom: 3rem !important;
    }
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

# --- 1. HERO (Full Screen) ---
st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">Kessy Yako Studio</h1>
        <p class="hero-subtitle">Web Design</p>
        <div class="scroll-down">↓</div>
    </div>
""", unsafe_allow_html=True)


# --- 2. OBSAH ---
with st.container():
    st.markdown('<div class="content-container">', unsafe_allow_html=True)

    # A) AI NÁSTROJ
    st.markdown("<h2>AI Kariérní Nástroj</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        job = st.text_area("INZERÁT", height=200, placeholder="Vložte text inzerátu...")
    with col2:
        cv = st.file_uploader("CV (PDF)", type="pdf")
        st.info("💡 Tip: AI vytvoří dopis na míru.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tlačítko uprostřed
    _, col_btn, _ = st.columns([1,2,1])
    with col_btn:
        if st.button("✨ VYGENEROVAT PROFESIONÁLNÍ DOPIS", use_container_width=True):
            if job and cv:
                with st.spinner("Pracuji..."):
                    try:
                        txt = get_pdf_text(cv)
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        res = model.generate_content(f"Napiš motivační dopis. Inzerát: {job}. CV: {txt}")
                        st.markdown(f"<div style='background:#111; padding:20px; border:1px solid #333; margin-top: 20px;'>{res.text}</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Chyba: {e}")

    st.markdown("<br><br><hr style='border-color: #333;'><br><br>", unsafe_allow_html=True)

    # B) SLUŽBY (3 KARTY)
    st.markdown("<h2>Co nabízíme</h2>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("### 🎨 Webdesign")
        st.write("Luxusní vizuální identita. Tvoříme weby, které budují důvěru a prodávají.")
    
    with c2:
        st.markdown("### 💻 Development")
        st.write("Robustní systémy. E-shopy a aplikace na míru s důrazem na rychlost.")
    
    with c3:
        st.markdown("### 🤖 AI Integrace")
        st.write("Automatizace procesů. Zapojte umělou inteligenci do vašeho podnikání.")

    st.markdown("<br><br><hr style='border-color: #333;'><br><br>", unsafe_allow_html=True)

    # C) KONTAKT
    st.markdown("<h2>Spolupráce</h2>", unsafe_allow_html=True)
    
    contact_form = """
    <form action="https://formspree.io/f/mpwvwwbj" method="POST">
        <input type="email" name="email" placeholder="Váš email" style="width: 100%; padding: 15px; margin-bottom: 10px; background: #0a0a0a; border: 1px solid #333; color: white;">
        <textarea name="message" rows="4" placeholder="Zpráva..." style="width: 100%; padding: 15px; margin-bottom: 20px; background: #0a0a0a; border: 1px solid #333; color: white;"></textarea>
        <button type="submit" style="width: 100%; padding: 15px; background: #f0f0f0; color: black; font-weight: bold; border: none; cursor: pointer;">ODESLAT</button>
    </form>
    """
    st.markdown(contact_form, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)