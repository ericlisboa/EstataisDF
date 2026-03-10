import streamlit as st
import os

# 1. Configuração da página
st.set_page_config(page_title="Download do Boletim", layout="wide")

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