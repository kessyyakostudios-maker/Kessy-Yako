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
    /* Import fontu Playfair Display */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap');

    /* 1. 3D POZADÍ (Radiální gradient) */
    .stApp {
        background: radial-gradient(circle at center, #1a1a1a 0%, #000000 100%);
        color: #e0e0e0;
    }

    /* 2. TYPOGRAFIE */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #e0e0e0 !important;
    }
    p, label, div {
        color: #cccccc;
    }

    /* 3. STŘÍBRNÁ TLAČÍTKA (Metalický efekt) */
    .stButton > button {
        background: linear-gradient(145deg, #e6e6e6, #b3b3b3) !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 5px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(145deg, #ffffff, #d9d9d9) !important;
        transform: scale(1.02) !important;
        box-shadow: 0 6px 8px rgba(0,0,0,0.5) !important;
    }
    .stButton > button:active {
        background: #a0a0a0 !important;
    }
    
    /* Odkazová tlačítka (Link Button) - stejný styl */
    a[kind="header"] {
        background: linear-gradient(145deg, #e6e6e6, #b3b3b3) !important;
        color: #000000 !important;
        font-weight: bold !important;
        text-decoration: none !important;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }

    /* 4. INPUTY (Tmavé pole) */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #111111 !important;
        color: white !important;
        border: 1px solid #333 !important;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #e0e0e0 !important;
        box-shadow: 0 0 5px rgba(224, 224, 224, 0.5) !important;
    }

    /* 5. SKRYTÍ MENU A REKLAM (Clean Look) */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .stDeployButton {display:none !important;}
    
    </style>
""", unsafe_allow_html=True)

# --- LOGIKA APLIKACE (AI) ---

# Načtení API klíče ze Secrets (aby to fungovalo online)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Chybí API klíč! Nastavte ho v Streamlit Secrets.")

# Funkce pro získání textu z PDF
def get_pdf_text(pdf_file):
    text = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# --- OBSAH WEBU ---

# Hlavní nadpis
st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>Vytvořte si perfektní motivační dopis pomocí AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-bottom: 4rem;'>Nahrajte své CV a inzerát práce. AI vytvoří profesionální dopis za vás.</p>", unsafe_allow_html=True)

# Vstupy pro AI
job_ad = st.text_area("TEXT INZERÁTU PRÁCE", placeholder="Vložte text pracovní nabídky...", height=150)
uploaded_file = st.file_uploader("VAŠE CV", type="pdf", label_visibility="visible")

# Tlačítko Generovat
if st.button("GENEROVAT MOTIVAČNÍ DOPIS", use_container_width=True):
    if job_ad and uploaded_file:
        with st.spinner("AI pracuje..."):
            try:
                # 1. Přečíst PDF
                cv_text = get_pdf_text(uploaded_file)
                
                # 2. Vybrat model (Robustní metoda)
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                # Zkusíme najít Flash, jinak bereme první dostupný
                model_name = next((m for m in available_models if 'flash' in m), available_models[0])
                model = genai.GenerativeModel(model_name)

                # 3. Prompt
                prompt = f"""
                Jsi profesionální kariérní poradce. Napiš přesvědčivý motivační dopis.
                
                INZERÁT: {job_ad}
                
                MÉ CV (TEXT): {cv_text}
                
                POKYNY:
                - Buď stručný, profesionální a sebevědomý.
                - Vypíchni mé zkušenosti, které se hodí k inzerátu.
                - Nepoužívej fráze jako "jsem ideální kandidát", ukaž to na příkladech.
                - Piš česky.
                """
                
                # 4. Generování
                response = model.generate_content(prompt)
                
                # 5. Výsledek
                st.success("Motivační dopis byl úspěšně vygenerován!")
                st.markdown("### Váš motivační dopis")
                st.markdown(response.text) # Markdown pro hezké formátování
                
                st.download_button(
                    label="Stáhnout jako text",
                    data=response.text,
                    file_name="motivacni_dopis.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"Došlo k chybě: {str(e)}")
    else:
        st.warning("Prosím vložte text inzerátu a nahrajte PDF životopis.")

st.markdown("---")

# --- SEKCE SLUŽBY (KARTY S ODKAZY) ---
st.markdown("<h2 style='text-align: center; margin-top: 3rem;'>Chcete vlastní web nebo AI aplikaci?</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-bottom: 3rem;'>Vytvářím digitální produkty na míru – od elegantních webů po pokročilé AI nástroje.</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Webdesign & UI")
    st.write("Vizuální identita. Vytváříme digitální zážitky, které oslovují a zanechávají trvalý dojem.")
    st.link_button("Zjistit více", "https://google.com") # Změň odkaz dle potřeby

with col2:
    st.markdown("### Development")
    st.write("Technická preciznost. Stavíme na solidních základech s důrazem na výkon a škálovatelnost.")
    st.link_button("Zjistit více", "https://google.com")

with col3:
    st.markdown("### AI Aplikace")
    st.write("Automatizace procesů. Integrujeme umělou inteligenci do vašeho podnikání pro efektivnější workflow.")
    st.link_button("Zjistit více", "https://google.com")

st.markdown("---")

# --- KONTAKTNÍ FORMULÁŘ (HTML FIX) ---
st.markdown("<h2 style='text-align: center;'>Napište mi o spolupráci</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-bottom: 2rem;'>Pojďme společně vytvořit něco výjimečného.</p>", unsafe_allow_html=True)

# HTML Formulář pro Formspree
contact_form = """
<form action="https://formspree.io/f/mpwvwwbj" method="POST">
    <div style="margin-bottom: 1.5rem;">
        <label style="display: block; margin-bottom: 0.75rem; color: #ccc;">Jméno</label>
        <input type="text" name="name" required placeholder="Vaše jméno" 
        style="width: 100%; padding: 12px; background-color: #111; border: 1px solid #333; color: white; border-radius: 5px;">
    </div>
    <div style="margin-bottom: 1.5rem;">
        <label style="display: block; margin-bottom: 0.75rem; color: #ccc;">Email</label>
        <input type="email" name="email" required placeholder="vas@email.cz" 
        style="width: 100%; padding: 12px; background-color: #111; border: 1px solid #333; color: white; border-radius: 5px;">
    </div>
    <div style="margin-bottom: 1.5rem;">
        <label style="display: block; margin-bottom: 0.75rem; color: #ccc;">Zpráva</label>
        <textarea name="message" rows="5" required placeholder="Popište mi váš projekt..." 
        style="width: 100%; padding: 12px; background-color: #111; border: 1px solid #333; color: white; border-radius: 5px;"></textarea>
    </div>
    <button type="submit" 
    style="width: 100%; padding: 14px; background: linear-gradient(145deg, #e6e6e6, #b3b3b3); color: black; font-weight: bold; border: none; border-radius: 5px; cursor: pointer;">
    ODESLAT ZPRÁVU
    </button>
</form>
"""

col_spacer, col_form, col_spacer2 = st.columns([1, 2, 1])
with col_form:
    st.markdown(contact_form, unsafe_allow_html=True)

# Patička (Logo)
st.markdown("<br><br><h1 style='text-align: center; color: #333 !important;'>KY</h1>", unsafe_allow_html=True)