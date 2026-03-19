import streamlit as st
import os

# 1. Configuração da página
st.set_page_config(page_title="Download do Boletim", layout="wide")

# --- NOVO BLOCO DE CSS PARA PADRONIZAÇÃO ---
st.markdown("""
<style>
    /* 1. FUNDO BRANCO */
    [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF !important;
    }

    /* 2. TÍTULOS EM LARANJA */
    h1, h2, h3, h4, h5, h6, [data-testid="stHeader"], .stHeader {
        color: #fb8c00 !important;
    }
    
    /* Ajuste da cor da linha divisória (divider) para laranja */
    hr {
        border-top-color: #fb8c00 !important;
    }

    /* 3. BOTÕES LARANJAS */
    div.stButton > button {
        background-color: #fb8c00 !important;
        color: #FFFFFF !important;
        border: none;
        font-weight: bold;
    }

    /* 4. TEXTOS GERAIS EM CINZA ESCURO */
    [data-testid="stWidgetLabel"], .stMarkdown {
        color: #2F2F2F !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. Definição dos caminhos
base_path = os.path.dirname(os.path.dirname(__file__))
pdf_path = os.path.join(base_path, "Boletim_das_Estatais_Distritais.pdf")

st.title("📄 Boletim das Estatais Distritais")
st.header("Acesso ao Documento Completo", divider="orange")

st.markdown("""
Nesta seção, você pode baixar a versão integral do **Boletim das Estatais Distritais**. 
O documento contém tabelas detalhadas, metodologias aplicadas e análises complementares 
sobre o desempenho das empresas públicas do DF.
""")

# 3. Verificação e Interface de Download
if os.path.exists(pdf_path):
    # Criando um layout centralizado para o botão
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.info("O arquivo está pronto para download.")
        
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
            
        st.download_button(
            label="📥 CLIQUE AQUI PARA BAIXAR O BOLETIM (PDF)",
            data=pdf_bytes,
            file_name="Boletim_das_Estatais_Distritais.pdf",
            mime="application/pdf",
            width='stretch' # Atualizado conforme os logs do seu servidor
        )
        
        st.caption("Tamanho do arquivo: Aproximadamente 2MB. Recomendamos o uso de um leitor de PDF atualizado.")
else:
    st.error("⚠️ Documento não encontrado no servidor.")
    st.info("O arquivo 'Boletim_das_Estatais_Distritais.pdf' não foi localizado na pasta raiz do projeto.")
