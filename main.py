import streamlit as st
st.title("🚀 StudyFlow.ai")
st.write("Le système est enfin libre !")
nom = st.text_input("Ton nom :")
if nom:
    st.success(f"Salut {nom} ! On va enfin pouvoir bosser.")
