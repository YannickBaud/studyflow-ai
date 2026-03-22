import streamlit as st
import google.generativeai as genai

# On récupère ta clé secrète configurée dans les Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # On utilise la version Pro pour laquelle tu as un abonnement
    model = genai.GenerativeModel('gemini-1.5-pro')
else:
    st.error("❌ La clé API n'est pas trouvée dans les Secrets. Vérifie l'étape précédente !")

st.set_page_config(page_title="StudyFlow.ai", page_icon="🚀")

st.title("🚀 StudyFlow.ai")
st.markdown("---")

st.subheader("🤖 Ton assistant d'étude personnel")
st.write("Pose-moi une question sur tes cours ou demande-moi un plan de révision.")

# Zone de saisie
user_input = st.text_input("Ta question :", placeholder="Ex: Explique-moi le théorème de Pythagore simplement...")

if user_input:
    with st.spinner("L'IA réfléchit..."):
        try:
            # L'IA génère la réponse
            response = model.generate_content(user_input)
            st.markdown("### 📝 Ma réponse :")
            st.info(response.text)
        except Exception as e:
            st.error(f"Oups, une erreur : {e}")

st.markdown("---")
st.caption("StudyFlow.ai v0.1 - Propulsé par Gemini 1.5 Pro")
