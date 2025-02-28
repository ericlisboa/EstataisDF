# Importando as bibliotecas
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import os
from PIL import Image

# Função para converter uma imagem em base64
def get_base64_of_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Função para definir a imagem de fundo
def set_background(image_path):
    base64_image = get_base64_of_image(image_path)
    
    # CSS para adicionar a imagem de fundo sem alterar o cabeçalho e sidebar
    page_bg_img = f"""
    <style>
    /* Aplicar imagem de fundo apenas ao container principal */
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpeg;base64,{base64_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    /* Remover a cor de fundo do cabeçalho para manter seu estilo original */
    [data-testid="stHeader"] {{
        background-color: transparent !important;
    }}
    
    /* Remover a cor de fundo da barra lateral para manter seu estilo original */
    [data-testid="stSidebar"] {{
        background-color: transparent !important;
    }}
    
    /* Manter o fundo principal com uma camada semitransparente para legibilidade */
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 10px;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Configurações da página
st.set_page_config(
    page_title="Estatais Distritais",
    page_icon="📈",  # Alterado o ícone para gráfico de linha
    layout="wide",
    initial_sidebar_state="expanded"
)

# Caminho base para a pasta do projeto
base_path = r"C:\Users\Eric\OneDrive\Estudos\RBCIP\Estatais\Dashboard\Arquivos VS Code\Painel.ST"

# Adicionar logomarcas no sidebar
with st.sidebar:
        
    # Caminho para as imagens das logomarcas
    logo_rbcip_path = os.path.join(base_path, "logorbcip.png")
    logo_fap_path = os.path.join(base_path, "logofap.png")
        
    # Verificar e exibir a logo da FAP
    if os.path.exists(logo_fap_path):
        st.image(logo_fap_path, width=200, caption="")
    else:
        st.warning("Logo FAP-DF não encontrada")
    
    # Adicionar um pequeno espaço entre as logos
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Verificar e exibir a logo da RBCIP
    if os.path.exists(logo_rbcip_path):
        st.image(logo_rbcip_path, width=200, caption="")
    else:
        st.warning("Logo RBCIP não encontrada")

# Caminho para a imagem de fundo
bg_image_path = os.path.join(base_path, "background.jpg")

# Verificar se a imagem existe antes de tentar definir o fundo
if os.path.exists(bg_image_path):
    # Configurar a imagem como fundo
    set_background(bg_image_path)
else:
    st.warning("Imagem de fundo não encontrada. Verifique se o arquivo 'background.jpg' existe no diretório correto.")

# Título e introdução
st.title(":orange[As Empresas Estatais Distritais]")
st.header("Uma análise das empresas pertencentes ao Governo do Distrito Federal", divider="orange")

introducao = """
O presente painel tem como finalidade organizar, consolidar e disponibilizar de forma acessível os dados relativos às empresas estatais do Distrito Federal (DF). A iniciativa visa aumentar a transparência no relacionamento financeiro entre o Governo do DF e suas empresas públicas, permitindo uma visão detalhada sobre sua governança, estrutura e desempenho econômico-financeiro.

As informações apresentadas foram extraídas de fontes oficiais, incluindo declarações do Governo do Distrito Federal, demonstrações contábeis das empresas e bases de dados públicas acessíveis por meio de portais governamentais. O período analisado compreende os anos de 2020 a 2023, garantindo uma visão histórica e comparativa da evolução das estatais distritais.

Este estudo é resultado do trabalho da Rede Brasileira de Certificação, Pesquisa e Inovação (RBCIP), com o apoio da Fundação de Apoio à Pesquisa do Distrito Federal (FAP-DF) e do próprio Governo do Distrito Federal. A iniciativa reforça o compromisso dessas instituições com a transparência e a gestão baseada em dados, fornecendo insumos técnicos para subsidiar decisões estratégicas sobre o setor público.

Para viabilizar uma análise aprofundada, o painel inclui gráficos interativos e a possibilidade de download dos dados, facilitando o acesso às informações para pesquisadores, gestores públicos e demais interessados. Dessa forma, busca-se estimular discussões qualificadas sobre o desempenho e a gestão das estatais distritais, promovendo o aprimoramento das políticas públicas e o uso eficiente dos recursos do estado.

"""
st.markdown(introducao)

# Seção de navegação com botões
st.subheader("As informações deste painel foram organizadas nas seguintes seções:", divider="orange")
col1, col2 = st.columns(2)

with col1:
    if st.button("1. Quais são as estatais do DF?"):
        st.switch_page("pages/01_Quais_sao_as_estatais.py")
    if st.button("2. Como é a governança das empresas?"):
        st.switch_page("pages/02_Governanca_das_empresas.py")
    if st.button("3. Qual o resultado financeiro das estatais?"):
        st.switch_page("pages/03_Resultado_financeiro_estatais.py")

with col2:
    if st.button("4. Qual o resultado para o Governo do DF?"):
        st.switch_page("pages/04_Resultado_financeiro_governo_df.py")
    if st.button("5. Comparativo com outros Estados"):
        st.switch_page("pages/05_Comparativo_outros_estados.py")