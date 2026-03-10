import streamlit as st
import os
import base64

# Configuração da página para ocupar a tela toda
st.set_page_config(page_title="Visualizar Boletim", layout="wide")

# Caminho para o PDF (considerando que ele está na pasta raiz 'Painel.ST')
base_path = os.path.dirname(os.path.dirname(__file__))
pdf_path = os.path.join(base_path, "Boletim_das_Estatais_Distritais.pdf")

st.title("📄 Boletim das Estatais Distritais")
st.markdown("---")

def display_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    
    # PDF incorporado em um iframe que ocupa quase toda a altura da tela
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

if os.path.exists(pdf_path):
    # Botão de download rápido no topo
    with open(pdf_path, "rb") as file:
        st.download_button(
            label="📥 Baixar Documento Original",
            data=file,
            file_name="Boletim_das_Estatais_Distritais.pdf",
            mime="application/pdf",
        )
    
    # Exibição do PDF
    display_pdf(pdf_path)
else:
    st.error(f"Arquivo não encontrado em: {pdf_path}")
    st.info("Certifique-se de que o arquivo PDF está na pasta raiz do projeto.")