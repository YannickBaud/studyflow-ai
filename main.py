import streamlit as st
import google.generativeai as genai
import PyPDF2

st.set_page_config(page_title="StudyFlow.ai", page_icon="🚀")
st.title("🚀 StudyFlow.ai")

# 1. DÉTECTION 100% AUTOMATIQUE DU MOTEUR
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    try:
        # On récupère la liste EXACTE des modèles autorisés par ta clé
        modeles_dispos = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                modeles_dispos.append(m.name.replace('models/', ''))
        
        if modeles_dispos:
            # On cherche en priorité la génération 3 (2026)
            modele_choisi = modeles_dispos[0] # Par défaut, on prend le premier qui marche
            for m in modeles_dispos:
                if "gemini-3" in m:
                    modele_choisi = m
                    break
            
            model = genai.GenerativeModel(modele_choisi)
            st.success(f"🔌 Connecté au moteur Nouvelle Génération : {modele_choisi}")
        else:
            st.error("Aucun modèle génératif trouvé sur cette clé API.")
            st.stop()
            
    except Exception as e:
        st.error(f"Impossible de lister les modèles : {e}")
        st.stop()
else:
    st.error("Clé API manquante dans les Secrets")
    st.stop()

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
        with st.spinner(f"Le modèle {modele_choisi} lit ton cours..."):
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
