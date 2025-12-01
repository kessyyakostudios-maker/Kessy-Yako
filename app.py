import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# --- KONFIGURACE ---
st.set_page_config(page_title="Kessy Yako Studio", page_icon="✨", layout="wide", initial_sidebar_state="collapsed")

# --- CSS DESIGN (LUXUSNÍ) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600&display=swap');

    /* 1. POZADÍ A ZÁKLAD */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(at 50% 0%, #1a1a1a 0%, #000000 70%);
        color: #e0e0e0;
    }

    /* 2. TYPOGRAFIE */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #ffffff !important;
        letter-spacing: 1px;
    }
    p, label, div, span, li {
        font-family: 'Montserrat', sans-serif !important;
        color: #cccccc;
        font-weight: 300;
    }

    /* 3. VYSKAKOVACÍ OKNA (MODALS) - TMAVÉ POZADÍ */
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

    /* 4. TLAČÍTKA (ČITELNÁ) */
    .stButton > button {
        background: white !important;
        color: black !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        border-radius: 0px !important; /* Hranaté luxusní */
        border: none !important;
        padding: 1rem 2rem !important;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: #d4af37 !important; /* Zlatá při hoveru */
        color: white !important;
        transform: scale(1.02);
    }

    /* 5. INPUTY */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #0a0a0a !important;
        border: 1px solid #333 !important;
        color: white !important;
        font-family: 'Montserrat', sans-serif;
    }
    .stTextInput > div > div > input:focus {
        border-color: #d4af37 !important;
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

# --- MODALY (BOHATÝ OBSAH) ---

@st.dialog("WEBDESIGN & UI")
def show_web():
    st.markdown("### Design, který prodává")
    st.write("Specializujeme se na 'High-End' vizuál. Vaše konkurence bude vypadat levně.")
    
    c1, c2 = st.columns(2)
    with c1:
        st.image("https://images.unsplash.com/photo-1600607686527-6fb886090705?q=80&w=2000&auto=format&fit=crop", caption="Weby pro hotely a restaurace")
    with c2:
        st.image("https://images.unsplash.com/photo-1606857521015-7f9fcf423740?q=80&w=2000&auto=format&fit=crop", caption="E-commerce pro módu")
    
    st.markdown("#### Co dostanete:")
    st.markdown("""
    * **Psychologie barev:** Vybíráme tóny, které vzbuzují důvěru.
    * **Dark Mode:** Specializujeme se na tmavé, prémiové rozhraní.
    * **Animace:** Web se musí hýbat, ale nesmí rušit.
    """)

@st.dialog("DEVELOPMENT")
def show_dev():
    st.markdown("### Robustní systémy na míru")
    st.write("Nestačí vám krabicové řešení? Stavíme systémy, které rostou s vámi.")
    
    st.success("🚀 **E-shop na míru:** Zvládne 10 000 objednávek denně.")
    st.info("🔒 **Klientské portály:** Bezpečné zóny pro vaše zákazníky.")
    st.warning("⚡ **Rychlost:** Optimalizujeme kód pro načtení do 0.5s.")

    st.image("https://images.unsplash.com/photo-1555099962-4199c345e5dd?q=80&w=2000&auto=format&fit=crop", caption="Backend Dashboard")

@st.dialog("AI AUDIT ZDARMA")
def show_ai():
    st.markdown("### 🤖 Získejte okamžitou AI analýzu")
    st.write("Zadejte popis vašeho byznysu a AI vám hned teď poradí 3 věci, jak vydělat víc.")
    
    biz_desc = st.text_area("Co děláte? (Např. Prodávám kávu, Učím angličtinu...)", height=100)
    
    if st.button("ANALYZOVAT MŮJ BYZNYS"):
        if biz_desc:
            with st.spinner("AI přemýšlí..."):
                try:
                    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    model = genai.GenerativeModel(next((m for m in models if 'flash' in m), models[0]))
                    response = model.generate_content(f"Jsi byznys konzultant. Uživatel dělá: {biz_desc}. Napiš 3 konkrétní, krátké body, jak může využít AI nebo zlepšit web, aby víc vydělal. Buď stručný.")
                    st.markdown(f"<div style='background:#111; padding:20px; border:1px solid #d4af37;'>{response.text}</div>", unsafe_allow_html=True)
                except:
                    st.error("Chyba AI.")
        else:
            st.warning("Napište něco o sobě.")

# --- OBSAH WEBU ---

st.markdown("<h1 style='text-align: center; font-size: 5rem; margin-top: 2rem;'>KESSY YAKO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; letter-spacing: 3px; font-size: 1.2rem; margin-bottom: 5rem;'>DIGITAL STUDIO & AI LAB</p>", unsafe_allow_html=True)

# 1. AI NÁSTROJ (HERO)
st.markdown("### ⚡ Generátor Motivačních Dopisů")
st.write("Ušetřete hodiny psaní. Vložte inzerát, nahrajte CV a získejte text, který vám otevře dveře.")

col_in1, col_in2 = st.columns([1, 1])
with col_in1:
    job = st.text_area("TEXT INZERÁTU", height=200, placeholder="Zkopírujte sem nabídku práce...")
with col_in2:
    cv = st.file_uploader("VAŠE CV (PDF)", type="pdf")
    st.write("")
    st.write("💡 *Tip: AI analyzuje klíčová slova z inzerátu.*")

if st.button("✨ VYGENEROVAT DOPIS", use_container_width=True):
    if job and cv:
        with st.spinner("Generuji..."):
            try:
                txt = get_pdf_text(cv)
                models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                model = genai.GenerativeModel(next((m for m in models if 'flash' in m), models[0]))
                res = model.generate_content(f"Napiš motivační dopis česky. Inzerát: {job}. CV: {txt}")
                st.balloons()
                st.markdown(f"<div style='background:#111; padding:30px; border-radius:10px; margin-top:20px;'>{res.text}</div>", unsafe_allow_html=True)
                st.download_button("STÁHNOUT", res.text, "dopis.txt")
            except Exception as e:
                st.error(f"Chyba: {e}")
    else:
        st.warning("Vyplňte obě pole.")

st.markdown("<br><br><br>", unsafe_allow_html=True)

# 2. SLUŽBY
st.markdown("<h2 style='text-align: center; margin-bottom: 3rem;'>Co pro vás můžeme vytvořit?</h2>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.image("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1964&auto=format&fit=crop")
    st.markdown("#### Webdesign & UI")
    st.write("Luxusní weby, které budují důvěru. Žádné šablony, čistý design na míru.")
    if st.button("UKÁZAT DESIGNY", key="b1"): show_web()

with c2:
    st.image("https://images.unsplash.com/photo-1555099962-4199c345e5dd?q=80&w=2000&auto=format&fit=crop")
    st.markdown("#### Development")
    st.write("Stavíme robustní systémy. Od e-shopů po interní firemní aplikace.")
    if st.button("UKÁZAT SYSTÉMY", key="b2"): show_dev()

with c3:
    st.image("https://images.unsplash.com/photo-1677442136019-21780ecad995?q=80&w=1932&auto=format&fit=crop")
    st.markdown("#### AI Řešení")
    st.write("Automatizace, která šetří peníze. Zkuste si naši AI analýzu zdarma.")
    if st.button("VYZKOUŠET AI", key="b3"): show_ai()

st.markdown("<br><br><hr style='border-color: #333;'><br>", unsafe_allow_html=True)

# 3. KONTAKT
st.markdown("<h2 style='text-align: center;'>Napište nám</h2>", unsafe_allow_html=True)
contact_form = """
<form action="https://formspree.io/f/mpwvwwbj" method="POST" style="max-width: 600px; margin: 0 auto;">
    <input type="email" name="email" placeholder="Váš email" style="width: 100%; padding: 15px; margin-bottom: 10px; background: #0a0a0a; border: 1px solid #333; color: white;">
    <textarea name="message" rows="4" placeholder="Váš projekt..." style="width: 100%; padding: 15px; margin-bottom: 20px; background: #0a0a0a; border: 1px solid #333; color: white;"></textarea>
    <button type="submit" style="width: 100%; padding: 15px; background: white; color: black; font-weight: bold; border: none; cursor: pointer;">ODESLAT</button>
</form>
"""
st.markdown(contact_form, unsafe_allow_html=True)
st.markdown("<br><br><h1 style='text-align: center; opacity: 0.2; font-size: 2rem;'>KY</h1>", unsafe_allow_html=True)