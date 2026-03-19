import streamlit as st
import os

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Estatais Distritais",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. DEFINIÇÃO DE CAMINHOS
base_path = os.path.dirname(__file__)

# 3. CSS GLOBAL (Sidebar e Elementos de Interface)
st.markdown("""
<style>
    /* Fundo do App */
    [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF !important;
    }

    /* Títulos em Laranja */
    h1, h2, h3, h4, h5, h6, [data-testid="stHeader"] {
        color: #fb8c00 !important;
    }

    /* BARRA LATERAL (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #4F4F4F !important;
        border-right: 2px solid #fb8c00;
    }

    /* Texto da Sidebar em Branco */
    [data-testid="stSidebarNav"] span {
        color: #FFFFFF !important;
        font-weight: 500 !important;
    }

    /* Ícones da Sidebar em Branco */
    [data-testid="stSidebarNav"] svg {
        fill: #FFFFFF !important;
    }

    /* BOTÕES LARANJAS */
    div.stButton > button {
        background-color: #fb8c00 !important;
        color: #FFFFFF !important;
        border: none;
        font-weight: bold;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        background-color: #e67e22 !important;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# 4. SIDEBAR (Logomarcas)
with st.sidebar:
    logo_rbcip_path = os.path.join(base_path, "logorbcip.png")
    logo_fap_path = os.path.join(base_path, "logofap.png")
    
    col_s1, col_s2, col_s3 = st.columns([1, 8, 1])
    
    if os.path.exists(logo_rbcip_path):
        with col_s2:
            st.image(logo_rbcip_path, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if os.path.exists(logo_fap_path):
        with col_s2:
            st.image(logo_fap_path, use_container_width=True)

# 5. TÍTULO E INTRODUÇÃO (Com correção cirúrgica de cor)
st.title(":orange[As Empresas Estatais Distritais]")
st.header("Uma análise das empresas pertencentes ao Governo do Distrito Federal", divider="orange")

# Usamos HTML isolado para garantir que APENAS este texto fique escuro e legível
introducao_html = """
<div style="color: #2F2F2F !important; font-size: 1.15rem; line-height: 1.6; text-align: justify; font-family: sans-serif;">
    O presente painel tem como finalidade organizar, consolidar e disponibilizar de forma acessível os dados 
    relativos às empresas estatais do Distrito Federal (DF). A iniciativa visa aumentar a transparência 
    no relacionamento financeiro entre o Governo do DF e suas empresas públicas, permitindo uma visão 
    detalhada sobre sua governança, estrutura e desempenho econômico-financeiro.
    <br><br>
    As informações apresentadas foram extraídas de fontes oficiais, incluindo declarações do Governo do 
    Distrito Federal, demonstrações contábeis das empresas e bases de dados públicas acessíveis por meio 
    de portais governamentais. O período analisado compreende os anos de 2020 a 2023, garantindo uma 
    visão histórica e comparativa da evolução das estatais distritais.
</div>
"""
st.markdown(introducao_html, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 6. SEÇÃO DE NAVEGAÇÃO (Botões de Atalho)
st.subheader("As informações deste painel foram organizadas nas seguintes seções:", divider="orange")

col1, col2 = st.columns(2)

with col1:
    if st.button("1. Quais são as estatais do DF?", use_container_width=True):
        st.switch_page("pages/01_Quais_sao_as_estatais_do_DF.py")
        
    if st.button("2. Como é a governança das empresas?", use_container_width=True):
        st.switch_page("pages/02_Governanca_das_empresas.py")
        
    if st.button("3. Qual o resultado financeiro das estatais?", use_container_width=True):
        st.switch_page("pages/03_Resultado_financeiro_estatais.py")

with col2:
    if st.button("4. Qual o resultado para o Governo do DF?", use_container_width=True):
        st.switch_page("pages/04_Resultado_financeiro_governo_df.py")
        
    if st.button("5. Comparativo com outros Estados", use_container_width=True):
        st.switch_page("pages/05_Comparativo_outros_estados.py")
        
    if st.button("6. Boletim das Estatais (Download)", use_container_width=True):
        st.switch_page("pages/06_Boletim_Completo.py")
