import streamlit as st
import os

# 1. CONFIGURAÇÃO DA PÁGINA (Deve ser o primeiro comando)
st.set_page_config(
    page_title="Estatais Distritais",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. DEFINIÇÃO DE CAMINHOS (Essencial estar aqui em cima para evitar o NameError)
base_path = os.path.dirname(__file__)

# 3. CSS para Sidebar Profissional e Títulos Laranjas
page_bg_img = """
<style>
    /* 1. FUNDO DO APP */
    [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF !important;
    }

    /* 2. TÍTULOS PRINCIPAIS (Laranja) */
    h1, h2, h3, h4, h5, h6, [data-testid="stHeader"] {
        color: #fb8c00 !important;
    }

    /* 3. BARRA LATERAL (A área circulada na foto) */
    [data-testid="stSidebar"] {
        background-color: #4F4F4F !important; /* Um cinza mais robusto */
        border-right: 2px solid #fb8c00; /* Linha sutil laranja para separar */
    }

    /* Cor do texto dos itens do menu lateral */
    [data-testid="stSidebarNav"] span {
        color: #FFFFFF !important;
        font-weight: 500 !important;
        font-size: 1.05rem !important;
    }

    /* Cor do ícone ao lado do texto no menu */
    [data-testid="stSidebarNav"] svg {
        fill: #FFFFFF !important;
    }

    /* Destaque para a página que está selecionada no momento */
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background-color: rgba(251, 140, 0, 0.2) !important; /* Fundo laranja clarinho */
        border-radius: 5px;
    }
    
    [data-testid="stSidebarNav"] a[aria-current="page"] span {
        color: #fb8c00 !important; /* Texto laranja na página atual */
        font-weight: bold !important;
    }

    /* 4. BOTÕES LARANJAS (Para manter o padrão) */
    div.stButton > button {
        background-color: #fb8c00 !important;
        color: #FFFFFF !important;
        border: none;
    }
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# 4. SIDEBAR (Logomarcas)
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

# 5. TÍTULO E INTRODUÇÃO
st.title(":orange[As Empresas Estatais Distritais]")
st.header("Uma análise das empresas pertencentes ao Governo do Distrito Federal", divider="orange")

introducao = """
O presente painel tem como finalidade organizar, consolidar e disponibilizar de forma acessível os dados relativos às empresas estatais do Distrito Federal (DF). A iniciativa visa aumentar a transparência no relacionamento financeiro entre o Governo do DF e suas empresas públicas, permitindo uma visão detalhada sobre sua governança, estrutura e desempenho econômico-financeiro.

As informações apresentadas foram extraídas de fontes oficiais, incluindo declarações do Governo do Distrito Federal, demonstrações contábeis das empresas e bases de dados públicas acessíveis por meio de portais governamentais. O período analisado compreende os anos de 2020 a 2023, garantindo uma visão histórica e comparativa da evolução das estatais distritais.
"""
st.markdown(introducao)

# 6. SEÇÃO DE NAVEGAÇÃO
st.subheader("As informações deste painel foram organizadas nas seguintes seções:", divider="orange")
col1, col2 = st.columns(2)

# 6. SEÇÃO DE NAVEGAÇÃO (Segura contra erros de sistema)
st.subheader("As informações deste painel foram organizadas nas seguintes seções:", divider="orange")
col1, col2 = st.columns(2)

with col1:
    if st.button("1. Quais são as estatais do DF?", use_container_width=True):
        # Chama o arquivo limpo no GitHub
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
