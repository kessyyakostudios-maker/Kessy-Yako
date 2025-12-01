import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# --- KONFIGURACE (DŮLEŽITÉ: Layout 'centered' místo 'wide') ---
st.set_page_config(page_title="Kessy Yako Studio", page_icon="✨", layout="centered", initial_sidebar_state="collapsed")

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
    
    /* 2. SKRYTÍ LIŠTY */
    header {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    div[data-testid="stDecoration"] {display: none !important;}
    
    /* Reset paddingu */
    .main .block-container {
        padding-top: 2rem !important;
        max-width: 900px !important; /* ZÚŽENÍ CELÉHO WEBU NA STŘED */
    }

    /* 3. HERO SEKCE */
    .hero-container {
        height: 80vh; /* Trochu menší než celá, ať je vidět, že něco je dole */
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    
    .hero-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 4rem !important; /* Pevná velikost místo vw */
        color: #ffffff !important;
        letter-spacing: 2px;
        margin: 0;
        text-shadow: 0 10px 30px rgba(0,0,0,0.8);
    }
    
    .hero-subtitle {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 1.2rem !important;
        color: #888888 !important;
        letter-spacing: 5px;
        text-transform: uppercase;
        margin-top: 1rem;
    }

    /* 4. MODALY (VYSKAKOVACÍ OKNA) - TMAVÉ POZADÍ */
    div[data-testid="stDialog"] {
        background-color: #111111 !important;
        border: 1px solid #333;
    }
    div[data-testid="stDialog"] h1, div[data-testid="stDialog"] h2, div[data-testid="stDialog"] h3 {
        color: #fff !important;
    }
    div[data-testid="stDialog"] p, div[data-testid="stDialog"] li {
        color: #ccc !important;
    }

    /* 5. TLAČÍTKA (ČERNÉ PÍSMO) */
    .stButton > button {
        background: #f0f0f0 !important;
        color: #000000 !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 4px;
        padding: 1rem 2rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 100%;
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
    
    /* NADPISY SEKCÍ */
    h2 {
        font-family: 'Playfair Display', serif !important;
        font-size: 2.5rem !important;
        text-align: center;
        margin-bottom: 2rem !important;
        margin-top: 4rem !important;
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

# --- MODALY (OBSAH) ---
@st.dialog("WEBDESIGN & UI")
def show_web():
    st.markdown("### Design, který prodává")
    st.image("https://images.unsplash.com/photo-1600607686527-6fb886090705?q=80&w=2000&auto=format&fit=crop")
    st.markdown("Specializujeme se na 'High-End' vizuál. Vaše konkurence bude vypadat levně.")

@st.dialog("DEVELOPMENT")
def show_dev():
    st.markdown("### Robustní systémy na míru")
    st.image("https://images.unsplash.com/photo-1555099962-4199c345e5dd?q=80&w=2000&auto=format&fit=crop")
    st.markdown("Nestačí vám krabicové řešení? Stavíme systémy, které rostou s vámi.")

@st.dialog("AI AUDIT ZDARMA")
def show_ai():
    st.markdown("### 🤖 AI Analýza")
    st.write("Zadejte popis vašeho byznysu a AI vám poradí.")
    biz = st.text_input("Co děláte?")
    if st.button("ANALYZOVAT"):
        st.success("Tato funkce bude dostupná brzy.")

# --- 1. HERO SEKCE ---
st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">KESSY YAKO</h1>
        <p class="hero-subtitle">DIGITAL STUDIO & AI LAB</p>
        <div style="margin-top: 3rem; opacity: 0.5; font-size: 2rem;">↓</div>
    </div>
""", unsafe_allow_html=True)


# --- 2. AI KARIÉRNÍ NÁSTROJ ---
st.markdown("<h2>AI Kariérní Nástroj</h2>", unsafe_allow_html=True)
st.write("Vložte inzerát, nahrajte CV a získejte text, který vám otevře dveře.")

job = st.text_area("TEXT INZERÁTU", height=200, placeholder="Zkopírujte sem nabídku práce...")
cv = st.file_uploader("VAŠE CV (PDF)", type="pdf")

st.markdown("<br>", unsafe_allow_html=True)
if st.button("✨ VYGENEROVAT DOPIS", use_container_width=True):
    if job and cv:
        with st.spinner("Analyzuji..."):
            try:
                txt = get_pdf_text(cv)
                model = genai.GenerativeModel('gemini-1.5-flash')
                res = model.generate_content(f"Napiš motivační dopis česky. Inzerát: {job}. CV: {txt}")
                st.markdown(f"<div style='background:#111; padding:30px; border:1px solid #333; margin-top:20px;'>{res.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Chyba: {e}")

st.markdown("<br><br><hr style='border-color: #333;'><br>", unsafe_allow_html=True)


# --- 3. SLUŽBY ---
st.markdown("<h2>Co pro vás můžeme vytvořit?</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.image("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1964&auto=format&fit=crop")
    st.markdown("#### Webdesign")
    if st.button("UKÁZAT", key="b1"): show_web()

with col2:
    st.image("https://images.unsplash.com/photo-1555099962-4199c345e5dd?q=80&w=2000&auto=format&fit=crop")
    st.markdown("#### Development")
    if st.button("UKÁZAT", key="b2"): show_dev()

with col3:
    st.image("https://images.unsplash.com/photo-1677442136019-21780ecad995?q=80&w=1932&auto=format&fit=crop")
    st.markdown("#### AI Řešení")
    if st.button("UKÁZAT", key="b3"): show_ai()

st.markdown("<br><br><hr style='border-color: #333;'><br>", unsafe_allow_html=True)


# --- 4. KONTAKT ---
st.markdown("<h2>Spolupráce</h2>", unsafe_allow_html=True)

contact_form = """
<form action="https://formspree.io/f/mpwvwwbj" method="POST">
    <input type="email" name="email" placeholder="Váš email" style="width: 100%; padding: 15px; margin-bottom: 10px; background: #0a0a0a; border: 1px solid #333; color: white;">
    <textarea name="message" rows="4" placeholder="Váš projekt..." style="width: 100%; padding: 15px; margin-bottom: 20px; background: #0a0a0a; border: 1px solid #333; color: white;"></textarea>
    <button type="submit" style="width: 100%; padding: 15px; background: white; color: black; font-weight: bold; border: none; cursor: pointer;">ODESLAT</button>
</form>
"""
st.markdown(contact_form, unsafe_allow_html=True)
st.markdown("<br><br><h1 style='text-align: center; opacity: 0.2; font-size: 2rem;'>KY</h1>", unsafe_allow_html=True)