import streamlit as st
import google.generativeai as genai
import PyPDF2

st.set_page_config(page_title="StudyFlow.ai", page_icon="🚀")
st.title("🚀 StudyFlow.ai")

# 1. DÉTECTION AUTOMATIQUE DU MOTEUR IA
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    try:
        # L'IA demande à Google : "Quels modèles j'ai le droit d'utiliser ?"
        modeles_dispos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # On choisit le meilleur modèle disponible dans ta liste
        modele_choisi = "gemini-1.5-flash" # Sécurité par défaut
        for m in modeles_dispos:
            if "1.5-flash" in m:
                modele_choisi = m.replace('models/', '')
                break
        
        model = genai.GenerativeModel(modele_choisi)
        st.success(f"🔌 Connecté au moteur : {modele_choisi}")
        
    except Exception as e:
        st.error(f"Impossible de lister les modèles : {e}")
else:
    st.error("Clé API manquante dans les Secrets")

# 2. LA BIBLIOTHÈQUE (PDF)
with st.sidebar:
    st.header("📚 Ta Bibliothèque")
    uploaded_file = st.file_uploader("Envoie ton cours (PDF)", type="pdf")

if uploaded_file:
    reader = PyPDF2.PdfReader(uploaded_file)
    content = ""
    for page in reader.pages:
        content += page.extract_text()
    
    st.success("✅ Cours chargé avec succès !")
    
    if st.button("📝 Créer une fiche de révision"):
        with st.spinner("L'IA lit ton cours..."):
            try:
                prompt = f"Fais une fiche de révision avec Concepts clés, Formules et 3 questions sur ce cours : {content[:15000]}"
                response = model.generate_content(prompt)
                st.info(response.text)
            except Exception as e:
                st.warning(f"L'IA a eu un souci de génération : {e}")

# 3. LE CHAT
st.markdown("---")
user_q = st.text_input("Pose une question sur ton cours :")
if user_q:
    with st.spinner("L'IA réfléchit..."):
        try:
            resp = model.generate_content(user_q)
            st.write(resp.text)
        except Exception as e:
            st.warning(f"Erreur : {e}")
