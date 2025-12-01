import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# --- KONFIGURACE STRÁNKY ---
st.set_page_config(
    page_title="Kessy Yako Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS STYLY (DESIGN) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&display=swap');

    /* 1. POZADÍ (Jemný Mesh Gradient - vypadá lépe než kruh) */
    .stApp {
        background-color: #000000;
        background-image: 
            radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
            radial-gradient(at 50% 0%, hsla(225,39%,30%,0.3) 0, transparent 50%), 
            radial-gradient(at 100% 0%, hsla(339,49%,30%,0.3) 0, transparent 50%);
        color: #e0e0e0;
    }

    /* 2. TYPOGRAFIE */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #ffffff !important;
        text-shadow: 0 4px 10px rgba(0,0,0,0.8);
    }
    p, label, div, span {
        font-family: 'Montserrat', sans-serif;
        color: #cccccc;
    }

    /* 3. TLAČÍTKA (ČERNÝ TEXT NA STŘÍBRNÉ) - OPRAVA ČITELNOSTI */
    .stButton > button {
        background: linear-gradient(180deg, #f0f0f0 0%, #aaaaaa 100%) !important;
        color: #000000 !important; /* ČERNÁ BARVA PÍSMA NATVRDO */
        font-weight: 900 !important;
        border: none !important;
        border-radius: 4px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5) !important;
        padding: 0.8rem 1rem !important;
    }
    .stButton > button:hover {
        background: white !important;
        transform: scale(1.02);
        box-shadow: 0 6px 15px rgba(255,255,255,0.2) !important;
    }
    
    /* Styl pro st.link_button a dialog buttony */
    button[kind="primary"], button[kind="secondary"] {
        color: black !important;
    }

    /* 4. VYSKAKOVACÍ OKNA (MODALS) - ABY BYL VIDĚT TEXT */
    div[role="dialog"] {
        background-color: #1a1a1a !important;
        border: 1px solid #333;
        color: white !important;
    }
    div[role="dialog"] h1, div[role="dialog"] h2, div[role="dialog"] p {
        color: white !important;
    }

    /* 5. INPUTY (VELKÉ A MODERNÍ) */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #0a0a0a !important;
        color: white !important;
        border: 1px solid #444 !important;
        font-size: 1.1rem;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #ffffff !important;
    }

    /* 6. SCHOVAT STREAMLIT PRVKY */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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

# --- DIALOGY (Portfolio) ---
@st.dialog("Webdesign & UI")
def show_web():
    st.markdown("## Luxusní weby, které prodávají")
    st.write("Vytváříme design, který podtrhne vaši značku.")
    st.image("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1964&auto=format&fit=crop")
    st.info("Specializace: Dark Mode Design, Minimalismus, Animace.")

@st.dialog("Development")
def show_dev():
    st.markdown("## Systémy na míru")
    st.write("E-shopy, klientské portály a automatizace.")
    st.code("print('Code that works.')", language="python")
    st.success("Technologie: Python, React, AI Integrace.")

@st.dialog("AI Aplikace")
def show_ai():
    st.markdown("## Umělá inteligence v praxi")
    st.write("Tohle, co právě používáte, je jen začátek.")
    st.write("Umíme naučit AI číst vaše smlouvy, odpovídat zákazníkům nebo analyzovat data.")

# --- OBSAH WEBU ---

# 1. LOGO A HLAVIČKA
st.markdown("<h1 style='text-align: center; font-size: 4rem; letter-spacing: 5px; margin-top: 2rem;'>KESSY YAKO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; letter-spacing: 2px; margin-bottom: 5rem; opacity: 0.7;'>DIGITAL STUDIO & AI LAB</p>", unsafe_allow_html=True)

# 2. HERO SEKCE (AI NÁSTROJ - VELKÝ)
st.markdown("### ⚡ AI Kariérní Architekt")
st.markdown("Neztrácejte čas psaním. Vložte inzerát, nahrajte CV a nechte AI pracovat.")

# Rozložení - Žádné sloupce pro inputy, ať je to obrovské
job_ad = st.text_area("1. TEXT INZERÁTU (Zkopírujte sem celou nabídku práce)", height=250)
uploaded_file = st.file_uploader("2. VAŠE CV (PDF)", type="pdf")

# Obrovské tlačítko přes celou šířku
st.markdown("<br>", unsafe_allow_html=True)
if st.button("✨ VYGENEROVAT MOTIVAČNÍ DOPIS ✨", use_container_width=True):
    if job_ad and uploaded_file:
        with st.spinner("Analyzuji profil a píšu text..."):
            try:
                text = get_pdf_text(uploaded_file)
                models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                model = genai.GenerativeModel(next((m for m in models if 'flash' in m), models[0]))
                
                response = model.generate_content(f"Napiš skvělý motivační dopis česky. Inzerát: {job_ad}. CV data: {text}")
                
                st.balloons()
                st.markdown("### 📄 Váš výsledek")
                st.markdown(f"<div style='background: #111; padding: 2rem; border-radius: 10px; border: 1px solid #333;'>{response.text}</div>", unsafe_allow_html=True)
                st.download_button("STÁHNOUT TEXT", response.text, "dopis.txt")
            except Exception as e:
                st.error(f"Chyba: {e}")
    else:
        st.warning("Vyplňte prosím obě pole výše.")

st.markdown("<br><br><br>", unsafe_allow_html=True)

# 3. SEKCE SLUŽBY (3 KARTY)
st.markdown("<h2 style='text-align: center; margin-bottom: 3rem;'>Naše další projekty</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Webdesign & UI")
    st.write("Estetika, která prodává. Weby pro prémiové značky.")
    if st.button("UKÁZAT PRÁCE", key="btn1"):
        show_web()

with col2:
    st.markdown("#### Development")
    st.write("Robustní systémy a e-shopy na míru.")
    if st.button("UKÁZAT SYSTÉMY", key="btn2"):
        show_dev()

with col3:
    st.markdown("#### AI Aplikace")
    st.write("Automatizace a nástroje nové generace.")
    if st.button("UKÁZAT AI", key="btn3"):
        show_ai()

st.markdown("<br><br><hr style='border-color: #333;'><br>", unsafe_allow_html=True)

# 4. KONTAKT
st.markdown("<h2 style='text-align: center;'>Spolupráce</h2>", unsafe_allow_html=True)

contact_form = """
<form action="https://formspree.io/f/mpwvwwbj" method="POST" style="max-width: 600px; margin: 0 auto;">
    <input type="email" name="email" required placeholder="Váš email" style="width: 100%; padding: 15px; margin-bottom: 10px; background: #111; border: 1px solid #333; color: white; border-radius: 5px;">
    <textarea name="message" rows="4" required placeholder="Jak vám můžeme pomoci?" style="width: 100%; padding: 15px; margin-bottom: 20px; background: #111; border: 1px solid #333; color: white; border-radius: 5px;"></textarea>
    <button type="submit" style="width: 100%; padding: 15px; background: #e0e0e0; color: black; font-weight: bold; border: none; border-radius: 5px; cursor: pointer;">ODESLAT</button>
</form>
"""
st.markdown(contact_form, unsafe_allow_html=True)
st.markdown("<br><br><br>", unsafe_allow_html=True)