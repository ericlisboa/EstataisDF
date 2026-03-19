import streamlit as st
import os
import base64

# 1. CONFIGURAÇÃO DA PÁGINA (Sempre o primeiro comando Streamlit)
st.set_page_config(
    page_title="Estatais Distritais",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CSS para fundo branco e forçar cores de texto escuras
page_bg_img = """
<style>
    /* 1. Fundo do App */
    [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF !important;
    }

    /* 2. Container de Conteúdo */
    .main .block-container {
        background-color: #FFFFFF;
        padding-top: 2rem;
    }

    /* 3. FORÇAR CORES DE TEXTO (Resolução da legibilidade) */
    /* Títulos e Subtítulos */
    h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2 {
        color: #1E1E1E !important; 
    }

    /* Texto comum e parágrafos */
    p, span, label, .stMarkdown p {
        color: #31333F !important;
    }

    /* Ajuste para as linhas divisórias (divider) */
    hr {
        border-color: #fb8c00 !important; /* Mantém o laranja da sua marca */
    }

    /* 4. Ajustes para dispositivos móveis */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        .stButton>button {
            width: 100%;
            margin-bottom: 10px;
        }
    }
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# 3. SIDEBAR (Logomarcas)
with st.sidebar:
    logo_rbcip_path = os.path.join(base_path, "logorbcip.png")
    logo_fap_path = os.path.join(base_path, "logofap.png")
    
    col1, col2, col3 = st.columns([1, 7, 1])
    
    if os.path.exists(logo_rbcip_path):
        with col2:
            st.image(logo_rbcip_path, width=300)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    if os.path.exists(logo_fap_path):
        with col2:
            st.image(logo_fap_path, width=300)

# 4. TÍTULO E INTRODUÇÃO
st.title(":orange[As Empresas Estatais Distritais]")
st.header("Uma análise das empresas pertencentes ao Governo do Distrito Federal", divider="orange")

introducao = """
O presente painel tem como finalidade organizar, consolidar e disponibilizar de forma acessível os dados relativos às empresas estatais do Distrito Federal (DF). A iniciativa visa aumentar a transparência no relacionamento financeiro entre o Governo do DF e suas empresas públicas, permitindo uma visão detalhada sobre sua governança, estrutura e desempenho econômico-financeiro.

As informações apresentadas foram extraídas de fontes oficiais, incluindo declarações do Governo do Distrito Federal, demonstrações contábeis das empresas e bases de dados públicas acessíveis por meio de portais governamentais. O período analisado compreende os anos de 2020 a 2023, garantindo uma visão histórica e comparativa da evolução das estatais distritais.
"""
st.markdown(introducao)

# 5. SEÇÃO DE NAVEGAÇÃO
st.subheader("As informações deste painel foram organizadas nas seguintes seções:", divider="orange")
col1, col2 = st.columns(2)

with col1:
    if st.button("1. Quais são as estatais do DF?", width='stretch'):
        st.switch_page("pages/01_Quais_sao_as_estatais.py")
    if st.button("2. Como é a governança das empresas?", width='stretch'):
        st.switch_page("pages/02_Governanca_das_empresas.py")
    if st.button("3. Qual o resultado financeiro das estatais?", width='stretch'):
        st.switch_page("pages/03_Resultado_financeiro_estatais.py")

with col2:
    if st.button("4. Qual o resultado para o Governo do DF?", width='stretch'):
        st.switch_page("pages/04_Resultado_financeiro_governo_df.py")
    if st.button("5. Comparativo com outros Estados", width='stretch'):
        st.switch_page("pages/05_Comparativo_outros_estados.py")
    if st.button("6. Boletim das Estatais (Download)", width='stretch'):
        st.switch_page("pages/06_Boletim_Completo.py")
