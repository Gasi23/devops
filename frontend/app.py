import streamlit as st
import requests

API_URL = "http://backend:8000"

st.title("📣 Plataforma de Feedback Estudantil")

menu = ["Enviar Feedback", "Ver Feedbacks"]
escolha = st.sidebar.selectbox("Navegação", menu)

if escolha == "Enviar Feedback":
    st.subheader("📝 Enviar feedback anônimo")
    texto = st.text_area("Digite seu feedback:")
    if st.button("Enviar"):
        if texto.strip():
            resposta = requests.post(f"{API_URL}/feedback", json={"texto": texto})
            if resposta.status_code == 200:
                st.success("Feedback enviado com sucesso!")
            else:
                st.error("Erro ao enviar feedback.")
        else:
            st.warning("O campo de feedback está vazio.")

elif escolha == "Ver Feedbacks":
    st.subheader("📊 Feedbacks recebidos")
    resposta = requests.get(f"{API_URL}/feedbacks")
    if resposta.status_code == 200:
        dados = resposta.json()
        for fb in dados:
            st.markdown(f"- {fb['texto']}")
    else:
        st.error("Erro ao carregar feedbacks.")
