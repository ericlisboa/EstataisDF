import streamlit as st
import os

# 1. CONFIGURAÇÃO DA PÁGINA
# Deve ser o primeiro comando. Definimos o título da aba do navegador.
st.set_page_config(
    page_title="Estatais Distritais",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded" # Alterado para aparecer a barra lateral corrigida
)

# 2. DEFINIÇÃO DE NAVEGAÇÃO (A sugestão que faltava)
# Aqui mapeamos o "Nome do Arquivo" para o "Nome com Acento" que aparecerá no menu
pg = st.navigation({
    "Menu Principal": [
        st.Page("Início.py", title="🏠 Início", default=True)
    ],
    "Análises Detalhadas": [
        st.Page("pages/01_Quais_sao_as_estatais_do_DF.py", title="1. Quais são as estatais do DF?"),
        st.Page("pages/02_Governanca_das_empresas.py", title="2. Governança das empresas"),
        st.Page("pages/03_Resultado_financeiro_estatais.py", title="3. Resultado financeiro das estatais"),
        st.Page("pages/04_Resultado_financeiro_governo_df.py", title="4. Resultado para o Governo do DF"),
        st.Page("pages/05_Comparativo_outros_estados.py", title="5. Comparativo com outros Estados"),
        st.Page("pages/06_Boletim_Completo.py", title="6. Boletim das Estatais (Download)")
    ]
})

# 3. CSS COMPLETO (Cores da Sidebar + Correção do Texto Ilegível)
st.markdown("""
<style>
    /* Fundo Branco */
    [data-testid="stAppViewContainer"] { background-color: #FFFFFF !important; }

    /* TEXTO DOS PARÁGRAFOS (Resolve a ilegibilidade) */
    p, span, label, li, .stMarkdown {
        color: #1E1E1E !important; /* Grafite escuro quase preto */
        font-size: 1.05rem;
    }

    /* Títulos em Laranja */
    h1, h2, h3, h4, h5, h6 { color: #fb8c00 !important; }

    /* BARRA LATERAL */
    [data-testid="stSidebar"] {
        background-color: #4F4F4F !important; /* Cinza escuro */
        border-right: 3px solid #fb8c00;
    }
    
    /* Texto da Sidebar em Branco */
    [data-testid="stSidebarNav"] span, [data-testid="stSidebar"] p {
        color: #FFFFFF !important;
    }

    /* Botões Laranjas */
    div.stButton > button {
        background-color: #fb8c00 !important;
        color: #FFFFFF !important;
        border: none;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 4. EXECUTAR NAVEGAÇÃO
# Isso faz com que o conteúdo da página selecionada apareça
# Se estiver no Início, ele executa o código abaixo. Se clicar em outra, ele muda.
if pg.title == "🏠 Início":
    
    # Renderizar Logomarcas na Sidebar (Apenas no Início ou em todas)
    base_path = os.path.dirname(__file__)
    with st.sidebar:
        st.markdown("<br>", unsafe_allow_html=True)
        logo_rbcip = os.path.join(base_path, "logorbcip.png")
        logo_fap = os.path.join(base_path, "logofap.png")
        
        if os.path.exists(logo_rbcip): st.image(logo_rbcip, width=250)
        st.markdown("<br>", unsafe_allow_html=True)
        if os.path.exists(logo_fap): st.image(logo_fap, width=250)

    # 5. CONTEÚDO DA PÁGINA INICIAL
    st.title(":orange[As Empresas Estatais Distritais]")
    st.header("Uma análise das empresas pertencentes ao Governo do Distrito Federal", divider="orange")

    st.markdown("""
    O presente painel tem como finalidade organizar, consolidar e disponibilizar de forma acessível os dados relativos às empresas estatais do Distrito Federal (DF). A iniciativa visa aumentar a transparência no relacionamento financeiro entre o Governo do DF e suas empresas públicas, permitindo uma visão detalhada sobre sua governança, estrutura e desempenho econômico-financeiro.

    As informações apresentadas foram extraídas de fontes oficiais, incluindo declarações do Governo do Distrito Federal, demonstrações contábeis das empresas e bases de dados públicas acessíveis por meio de portais governamentais. O período analisado compreende os anos de 2020 a 2023, garantindo uma visão histórica e comparativa da evolução das estatais distritais.
    """)

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

else:
    # Isso executa as outras páginas quando clicadas na barra lateral
    pg.run()
