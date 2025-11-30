import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
import io

# Page config
st.set_page_config(
    page_title="AI Career Architect - Kessy Yako Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - převzatý luxusní tmavý styl z index.html
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Playfair Display', serif;
            font-weight: 400;
        }
        
        .stApp {
            background-color: #0a0a0a;
            color: #e5e5e5;
        }
        
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #111111;
        }
        
        [data-testid="stSidebar"] {
            background-color: #111111;
        }
        
        [data-testid="stSidebar"] .css-1d391kg {
            background-color: #111111;
        }
        
        /* Input fields */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background-color: #111111;
            color: #e5e5e5;
            border: 1px solid rgba(229, 229, 229, 0.2);
            border-radius: 0;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #d4af37;
            border-opacity: 0.5;
        }
        
        /* Buttons */
        .stButton > button {
            background-color: rgba(212, 175, 55, 0.1);
            color: #d4af37;
            border: 1px solid rgba(212, 175, 55, 0.3);
            border-radius: 0;
            font-weight: 300;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            padding: 0.75rem 2rem;
            transition: all 0.3s;
        }
        
        .stButton > button:hover {
            background-color: rgba(212, 175, 55, 0.2);
            border-color: #d4af37;
        }
        
        /* File uploader */
        .stFileUploader > div {
            background-color: #111111;
            border: 1px solid rgba(229, 229, 229, 0.2);
            border-radius: 0;
        }
        
        /* Text colors */
        .stMarkdown {
            color: #e5e5e5;
        }
        
        h1, h2, h3 {
            color: #e5e5e5;
        }
        
        .gold-text {
            color: #d4af37;
        }
        
        /* Service cards */
        .service-card {
            background-color: rgba(229, 229, 229, 0.02);
            border: 1px solid rgba(229, 229, 229, 0.1);
            padding: 2rem;
            margin: 1rem 0;
        }
        
        /* Contact form */
        .contact-section {
            border-top: 1px solid rgba(229, 229, 229, 0.1);
            padding-top: 3rem;
            margin-top: 3rem;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_key' not in st.session_state:
    st.session_state.api_key = ''
if 'cover_letter' not in st.session_state:
    st.session_state.cover_letter = ''

# Sidebar - API Key input
with st.sidebar:
    st.markdown("### KESSY YAKO")
    st.markdown("---")
    api_key = st.text_input(
        "Google API Key",
        type="password",
        value=st.session_state.api_key,
        help="Zadejte svůj Google Gemini API klíč"
    )
    st.session_state.api_key = api_key

# Main content
st.markdown("""
    <div style="text-align: center; padding: 4rem 0;">
        <h1 style="font-size: 3.5rem; margin-bottom: 1rem; font-weight: 400;">
            AI Career Architect
        </h1>
        <p style="font-size: 1.25rem; opacity: 0.7; font-weight: 300;">
            Vytvořte si perfektní motivační dopis pomocí AI
        </p>
    </div>
""", unsafe_allow_html=True)

# Hero Section - Input fields
st.markdown("### Text inzerátu práce")
job_ad = st.text_area(
    "Vložte text pracovní nabídky...",
    height=150,
    key="job_ad",
    label_visibility="collapsed"
)

st.markdown("### Vaše CV")
uploaded_file = st.file_uploader(
    "Nahrát CV (PDF)",
    type=['pdf'],
    key="cv_upload",
    label_visibility="collapsed"
)

if uploaded_file is not None:
    st.success(f"✓ Nahraný soubor: {uploaded_file.name}")

# Generate button
generate_button = st.button(
    "Generovat motivační dopis",
    type="primary",
    use_container_width=True
)

# Generate cover letter
if generate_button:
    if not st.session_state.api_key:
        st.error("⚠️ Prosím, zadejte Google API Key v sidebaru.")
    elif not job_ad.strip():
        st.error("⚠️ Prosím, vložte text inzerátu práce.")
    elif uploaded_file is None:
        st.error("⚠️ Prosím, nahrajte své CV (PDF).")
    else:
        with st.spinner("Generuji motivační dopis pomocí AI..."):
            try:
                # Read PDF
                pdf_bytes = uploaded_file.read()
                pdf_reader = PdfReader(io.BytesIO(pdf_bytes))
                cv_text = ""
                for page in pdf_reader.pages:
                    cv_text += page.extract_text() + "\n"
                
                if not cv_text.strip():
                    st.error("⚠️ Nepodařilo se přečíst text z PDF. Zkontrolujte, zda je soubor správně formátovaný.")
                else:
                    # Configure Gemini
                    genai.configure(api_key=st.session_state.api_key)
                    
                    try:
                        # Získat seznam všech dostupných modelů pro tento klíč
                        dostupne_modely = []
                        for m in genai.list_models():
                            if 'generateContent' in m.supported_generation_methods:
                                dostupne_modely.append(m.name)
                        
                        # Vybrat ten nejlepší (hledáme Flash)
                        vybrany_model = next((m for m in dostupne_modely if 'flash' in m.lower()), dostupne_modely[0] if dostupne_modely else None)
                        
                        if vybrany_model:
                            
                            # Create prompt
                            prompt = f"""Jsi seniorní HR expert. Napiš přesvědčivý motivační dopis pro uchazeče s tímto životopisem:

{cv_text}

na tuto pozici:

{job_ad}

Motivační dopis by měl být profesionální, přesvědčivý a přizpůsobený konkrétní pozici. Použij formální tón a strukturu klasického motivačního dopisu."""
                            
                            model = genai.GenerativeModel(vybrany_model)
                            response = model.generate_content(prompt)
                            cover_letter = response.text
                            st.session_state.cover_letter = cover_letter
                            
                            st.success("✓ Motivační dopis byl úspěšně vygenerován!")
                        else:
                            st.error("Tvůj API klíč nevidí žádné modely. Je klíč správný?")
                    
                    except Exception as e:
                        st.error(f"FATÁLNÍ CHYBA: {str(e)}")
                    
            except Exception as e:
                st.error(f"⚠️ Chyba při generování: {str(e)}")
                st.info("Zkontrolujte, zda je API klíč správný a máte přístup k Gemini API.")

# Display generated cover letter
if st.session_state.cover_letter:
    st.markdown("---")
    st.markdown("### Váš motivační dopis")
    st.markdown(f'<div style="background-color: #111111; padding: 2rem; border: 1px solid rgba(229, 229, 229, 0.2); line-height: 1.8; font-weight: 300; color: #e5e5e5;">', unsafe_allow_html=True)
    st.markdown(st.session_state.cover_letter)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Download button
    st.download_button(
        label="📥 Stáhnout jako .txt",
        data=st.session_state.cover_letter,
        file_name="motivacni_dopis.txt",
        mime="text/plain",
        use_container_width=True
    )

# Services Section
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 3rem 0;">
        <h2 style="font-size: 2.5rem; margin-bottom: 1rem; font-weight: 400;">
            Chcete vlastní web nebo AI aplikaci?
        </h2>
        <p style="font-size: 1.125rem; opacity: 0.7; font-weight: 300; max-width: 600px; margin: 0 auto 3rem;">
            Vytvářím digitální produkty na míru – od elegantních webů po pokročilé AI nástroje.
        </p>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="service-card">
            <h3 style="font-size: 1.75rem; margin-bottom: 1rem; color: #d4af37;">Webdesign & UI</h3>
            <p style="opacity: 0.7; margin-bottom: 0.5rem; font-weight: 300;">Vizuální identita</p>
            <p style="opacity: 0.6; font-size: 0.875rem; font-weight: 300; line-height: 1.6;">
                Vytváříme digitální zážitky, které oslovují a zanechávají trvalý dojem.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="service-card">
            <h3 style="font-size: 1.75rem; margin-bottom: 1rem; color: #d4af37;">Development</h3>
            <p style="opacity: 0.7; margin-bottom: 0.5rem; font-weight: 300;">Technická preciznost</p>
            <p style="opacity: 0.6; font-size: 0.875rem; font-weight: 300; line-height: 1.6;">
                Stavíme na solidních základech s důrazem na výkon a škálovatelnost.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="service-card">
            <h3 style="font-size: 1.75rem; margin-bottom: 1rem; color: #d4af37;">AI Aplikace</h3>
            <p style="opacity: 0.7; margin-bottom: 0.5rem; font-weight: 300;">Automatizace procesů</p>
            <p style="opacity: 0.6; font-size: 0.875rem; font-weight: 300; line-height: 1.6;">
                Integrujeme umělou inteligenci do vašeho podnikání pro efektivnější workflow.
            </p>
        </div>
    """, unsafe_allow_html=True)

# Contact Section
st.markdown("---")
st.markdown("""
    <div class="contact-section">
        <div style="text-align: center; margin-bottom: 3rem;">
            <h2 style="font-size: 2.5rem; margin-bottom: 1rem; font-weight: 400;">
                Napište mi o spolupráci
            </h2>
            <p style="font-size: 1.125rem; opacity: 0.7; font-weight: 300;">
                Pojďme společně vytvořit něco výjimečného.
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Contact form (using HTML form for Formspree)
st.markdown("""
    <form action="https://formspree.io/f/mpwvwwbj" method="POST" style="max-width: 600px; margin: 0 auto;">
        <div style="margin-bottom: 1.5rem;">
            <label style="display: block; margin-bottom: 0.75rem; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.7;">
                Jméno
            </label>
            <input 
                type="text" 
                name="name" 
                required 
                placeholder="Vaše jméno"
                style="width: 100%; background-color: #111111; border: 1px solid rgba(229, 229, 229, 0.2); padding: 1rem 1.5rem; color: #e5e5e5; font-family: 'Inter', sans-serif; font-weight: 300; border-radius: 0; box-sizing: border-box;"
            >
        </div>
        
        <div style="margin-bottom: 1.5rem;">
            <label style="display: block; margin-bottom: 0.75rem; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.7;">
                Email
            </label>
            <input 
                type="email" 
                name="email" 
                required 
                placeholder="vas@email.cz"
                style="width: 100%; background-color: #111111; border: 1px solid rgba(229, 229, 229, 0.2); padding: 1rem 1.5rem; color: #e5e5e5; font-family: 'Inter', sans-serif; font-weight: 300; border-radius: 0; box-sizing: border-box;"
            >
        </div>
        
        <div style="margin-bottom: 1.5rem;">
            <label style="display: block; margin-bottom: 0.75rem; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.7;">
                Zpráva
            </label>
            <textarea 
                name="message" 
                required 
                rows="6"
                placeholder="Popište mi váš projekt nebo dotaz..."
                style="width: 100%; background-color: #111111; border: 1px solid rgba(229, 229, 229, 0.2); padding: 1rem 1.5rem; color: #e5e5e5; font-family: 'Inter', sans-serif; font-weight: 300; border-radius: 0; box-sizing: border-box; resize: vertical;"
            ></textarea>
        </div>
        
        <button 
            type="submit"
            style="width: 100%; background-color: rgba(212, 175, 55, 0.1); border: 1px solid rgba(212, 175, 55, 0.3); padding: 1.25rem 2rem; color: #d4af37; font-family: 'Inter', sans-serif; font-weight: 300; letter-spacing: 0.1em; text-transform: uppercase; font-size: 0.875rem; cursor: pointer; transition: all 0.3s; border-radius: 0;"
            onmouseover="this.style.backgroundColor='rgba(212, 175, 55, 0.2)'"
            onmouseout="this.style.backgroundColor='rgba(212, 175, 55, 0.1)'"
        >
            Odeslat zprávu
        </button>
    </form>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="text-align: center; padding: 3rem 0; border-top: 1px solid rgba(229, 229, 229, 0.1); margin-top: 3rem;">
        <div style="font-family: 'Playfair Display', serif; font-size: 4rem; font-weight: 300; margin-bottom: 2rem;">
            KY
        </div>
        <a href="mailto:kessyyakostudios@gmail.com" style="color: #e5e5e5; text-decoration: none; font-size: 1.125rem; opacity: 0.8; transition: opacity 0.3s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.8'">
            kessyyakostudios@gmail.com
        </a>
        <p style="margin-top: 2rem; font-size: 0.875rem; opacity: 0.5; font-weight: 300;">
            © 2025 Kessy Yako Studio. All rights reserved.
        </p>
    </div>
""", unsafe_allow_html=True)


