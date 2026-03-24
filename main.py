import streamlit as st
import google.generativeai as genai
import PyPDF2

# Configuration avec ta clé secrète
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # On utilise le modèle universel, impossible qu'il fasse une erreur 404
    model = genai.GenerativeModel('gemini-pro')
else:
    st.error("Clé API manquante dans les Secrets")

st.set_page_config(page_title="StudyFlow.ai", page_icon="🚀")
st.title("🚀 StudyFlow.ai")

# Barre latérale pour l'envoi de fichiers
with st.sidebar:
    st.header("📚 Ta Bibliothèque")
    uploaded_file = st.file_uploader("Envoie ton cours (PDF)", type="pdf")

if uploaded_file:
    reader = PyPDF2.PdfReader(uploaded_file)
    content = ""
    for page in reader.pages:
        content += page.extract_text()
    
    st.success("✅ Cours chargé !")
    
    # Bouton d'action
    if st.button("📝 Créer une fiche de révision"):
        with st.spinner("L'IA lit ton cours... (ça peut prendre 10 secondes)"):
            try:
                # On limite le texte pour que l'IA ne s'étouffe pas
                prompt = f"Voici le contenu d'un cours : {content[:15000]}. Fais-moi une synthèse avec : Concepts clés, Formules importantes et 3 questions d'entraînement."
                response = model.generate_content(prompt)
                st.info(response.text)
            except Exception as e:
                st.warning(f"Oups, l'IA a eu un petit hoquet : {e}")

# Chat classique pour poser des questions
st.markdown("---")
user_q = st.text_input("Pose une question sur ton cours :")
if user_q:
    with st.spinner("L'IA réfléchit..."):
        try:
            resp = model.generate_content(user_q)
            st.write(resp.text)
        except Exception as e:
            st.warning(f"Erreur de réseau : {e}")
