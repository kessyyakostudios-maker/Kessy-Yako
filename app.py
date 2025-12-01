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

# --- CSS STYLY (DESIGN & ANIMACE) ---
st.markdown("""
    <style>
    /* Import fontu Playfair Display */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap');

    /* 1. ANIMACE (Fade In Up) */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translate3d(0, 40px, 0);
        }
        to {
            opacity: 1;
            transform: translate3d(0, 0, 0);
        }
    }

    /* Aplikace animace na hlavní kontejnery */
    .element-container, .stMarkdown, .row-widget {
        animation: fadeInUp 0.8s ease-out both;
    }

    /* 2. LEPŠÍ 3D POZADÍ (Jemnější gradient) */
    .stApp {
        background: radial-gradient(circle at 50% 30%, #2b2b2b 0%, #000000 90%);
        color: #e0e0e0;
    }

    /* 3. TYPOGRAFIE */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #e0e0e0 !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }
    p, label, div {
        color: #cccccc;
    }

    /* 4. TLAČÍTKA (ČERNÉ PÍSMO + STŘÍBRNÁ) */
    .stButton > button {
        background: linear-gradient(180deg, #ffffff 0%, #d1d1d1 100%) !important;
        color: #000000 !important; /* ČERNÁ BARVA PÍSMA */
        font-weight: 800 !important;
        border: none !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton > button:hover {
        background: linear-gradient(180deg, #ffffff 0%, #e6e6e6 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 255, 255, 0.15) !important;
    }
    .stButton > button:active {
        transform: translateY(1px) !important;
    }

    /* 5. INPUTY */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #0a0a0a !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 8px;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #e0e0e0 !important;
        box-shadow: 0 0 10px rgba(224, 224, 224, 0.2) !important;
    }

    /* 6. SKRYTÍ ZBYTEČNOSTÍ */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .stDeployButton {display:none !important;}
    
    </style>
""", unsafe_allow_html=True)

# --- LOGIKA APLIKACE (AI) ---

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    pass # Chybu vypíšeme až při akci

def get_pdf_text(pdf_file):
    text = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# --- FUNKCE PRO PORTFOLIO (VYSKAKOVACÍ OKNA) ---
@st.dialog("Webdesign & UI Portfolio")
def show_web_portfolio():
    st.markdown("### Ukázky naší práce")
    st.write("Specializujeme se na čistý, luxusní design, který prodává.")
    
    st.image("https://images.unsplash.com/photo-1467232004584-a241de8bcf5d?q=80&w=2069&auto=format&fit=crop", caption="Redesign e-shopu pro módní značku")
    st.image("https://images.unsplash.com/photo-1555421689-d68471e189f2?q=80&w=2070&auto=format&fit=crop", caption="Web pro michelinskou restauraci")
    st.markdown("**Zaujalo vás to?** Napište nám dole o spolupráci.")

@st.dialog("Development Projekty")
def show_dev_portfolio():
    st.markdown("### Technická řešení na míru")
    st.write("Stavíme robustní systémy, které zvládnou tisíce uživatelů.")
    
    st.info("🛠️ **Realitní portál:** Automatické stahování dat z katastru nemovitostí.")
    st.info("💳 **Fintech aplikace:** Bezpečné platby a klientská zóna.")
    st.markdown("Používáme nejmodernější technologie: Python, React, Next.js.")

@st.dialog("AI Implementace")
def show_ai_portfolio():
    st.markdown("### Automatizace budoucnosti")
    st.write("Šetříme firmám stovky hodin měsíčně pomocí AI agentů.")
    
    st.success("🤖 **AI Recepční:** Chatbot, který sám domlouvá schůzky 24/7.")
    st.success("📄 **Analyzátor smluv:** AI, které přečte smlouvu a upozorní na rizika.")
    st.write("To, co právě používáte (Generátor dopisů), je jen malá ukázka toho, co umíme.")

# --- OBSAH WEBU ---

# Hlavní nadpis s animací
st.markdown("<h1 style='text-align: center; margin-bottom: 1rem; font-size: 3.5rem;'>KESSY YAKO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-bottom: 4rem; font-size: 1.2rem;'>Digitální alchymie. Měníme kód v zážitky.</p>", unsafe_allow_html=True)

# --- ČÁST 1: AI NÁSTROJ ---
with st.container():
    st.markdown("<h3 style='text-align: center;'>Vyzkoušejte naše AI Demo</h3>", unsafe_allow_html=True)
    
    col_main1, col_main2 = st.columns([1, 1])
    
    with col_main1:
        job_ad = st.text_area("1. VLOŽTE TEXT INZERÁTU", placeholder="Zkopírujte sem text nabídky práce...", height=200)
    
    with col_main2:
        uploaded_file = st.file_uploader("2. NAHRAJTE SVÉ CV (PDF)", type="pdf")
        st.info("💡 Tip: Čím detailnější inzerát, tím lepší výsledek.")

    # Tlačítko Generovat (Centrované)
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("GENEROVAT MOTIVAČNÍ DOPIS", use_container_width=True):
            if job_ad and uploaded_file:
                with st.spinner("Analyzuji vaše zkušenosti a píšu dopis..."):
                    try:
                        cv_text = get_pdf_text(uploaded_file)
                        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                        model_name = next((m for m in available_models if 'flash' in m), available_models[0])
                        model = genai.GenerativeModel(model_name)

                        prompt = f"Jsi profesionál. Napiš motivační dopis česky. Inzerát: {job_ad}. CV: {cv_text}."
                        response = model.generate_content(prompt)
                        
                        st.balloons()
                        st.markdown("### ✨ Váš dopis je hotový")
                        st.markdown(response.text)
                        st.download_button("STÁHNOUT JAKO TEXT", response.text, "dopis.txt")
                        
                    except Exception as e:
                        st.error(f"Chyba: {str(e)}")
            else:
                st.warning("Prosím vyplňte obě pole.")

st.markdown("---")

# --- ČÁST 2: SLUŽBY & PORTFOLIO (MODALY) ---
st.markdown("<h2 style='text-align: center; margin-top: 3rem;'>Co pro vás můžeme vytvořit?</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-bottom: 3rem;'>Klikněte pro ukázku našich realizací.</p>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### Webdesign & UI")
    st.write("Weby, které se neodcházejí. Luxusní vizuál a psychologie prodeje.")
    if st.button("UKÁZAT REALIZACE", key="btn_web"):
        show_web_portfolio()

with c2:
    st.markdown("### Development")
    st.write("Aplikace na míru. E-shopy, portály a systémy, které fungují.")
    if st.button("UKÁZAT SYSTÉMY", key="btn_dev"):
        show_dev_portfolio()

with c3:
    st.markdown("### AI Řešení")
    st.write("Váš náskok před konkurencí. Chatboty a automatizace na míru.")
    if st.button("UKÁZAT AI NÁSTROJE", key="btn_ai"):
        show_ai_portfolio()

st.markdown("---")

# --- ČÁST 3: KONTAKT ---
st.markdown("<h2 style='text-align: center;'>Napište nám</h2>", unsafe_allow_html=True)

contact_form = """
<form action="https://formspree.io/f/mpwvwwbj" method="POST">
    <input type="text" name="name" required placeholder="Jméno" style="width: 100%; margin-bottom: 10px; padding: 15px; background: #111; border: 1px solid #333; color: white; border-radius: 5px;">
    <input type="email" name="email" required placeholder="Email" style="width: 100%; margin-bottom: 10px; padding: 15px; background: #111; border: 1px solid #333; color: white; border-radius: 5px;">
    <textarea name="message" rows="5" required placeholder="O čem je váš projekt?" style="width: 100%; margin-bottom: 20px; padding: 15px; background: #111; border: 1px solid #333; color: white; border-radius: 5px;"></textarea>
    <button type="submit" style="width: 100%; padding: 15px; background: linear-gradient(180deg, #fff, #ccc); color: black; font-weight: bold; border: none; border-radius: 5px; cursor: pointer;">ODESLAT POPTÁVKU</button>
</form>
"""

col_space_L, col_contact, col_space_R = st.columns([1, 2, 1])
with col_contact:
    st.markdown(contact_form, unsafe_allow_html=True)

st.markdown("<br><br><h1 style='text-align: center; opacity: 0.3;'>KY</h1>", unsafe_allow_html=True)